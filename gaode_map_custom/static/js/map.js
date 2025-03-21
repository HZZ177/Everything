// 全局变量
let map;
let markers = [];
let currentMode = 'view'; // 'view', 'add', 'edit', 'delete'
let activeCircleEditor = null;
let selectedMarker = null;
let clickListener = null; // 新增：用于跟踪地图点击事件监听器

// 初始化高德地图
function initMap() {
    // 设置安全密钥
    window._AMapSecurityConfig = {
        securityJsCode: window.AMAP_SECURITY_CODE,
    };

    // 初始化地图
    map = new AMap.Map('map-container', {
        zoom: 14,
        center: [104.06667, 30.66667], // 成都市中心
        viewMode: '2D'
    });

    console.log('地图初始化完成'); // 调试日志

    // 加载标记数据
    loadMarkers();

    // 设置工具栏按钮事件
    document.getElementById('add-marker-btn').addEventListener('click', toggleAddMode);
    document.getElementById('edit-markers-btn').addEventListener('click', toggleEditMode);
    document.getElementById('delete-markers-btn').addEventListener('click', toggleDeleteMode);

    // 地图点击事件会在toggleAddMode函数中动态添加和移除

    // 右键菜单事件绑定
    document.getElementById('edit-marker-menu').addEventListener('click', editSelectedMarker);
    document.getElementById('delete-marker-menu').addEventListener('click', deleteSelectedMarker);

    // 关闭图片预览
    document.getElementById('close-preview').addEventListener('click', closeImagePreview);

    // 关闭编辑对话框
    document.getElementById('close-edit-dialog').addEventListener('click', closeEditDialog);

    // 保存标记按钮
    document.getElementById('save-marker-btn').addEventListener('click', saveMarkerChanges);

    // 图片上传按钮
    document.getElementById('image-upload-btn').addEventListener('click', function() {
        document.getElementById('image-upload').click();
    });

    document.getElementById('image-upload').addEventListener('change', uploadImages);

    // 点击地图空白处关闭右键菜单
    document.addEventListener('click', function(e) {
        document.getElementById('marker-context-menu').style.display = 'none';
    });

    // 阻止右键菜单冒泡
    document.getElementById('marker-context-menu').addEventListener('click', function(e) {
        e.stopPropagation();
    });
}

// 加载标记数据
function loadMarkers() {
    fetch('/api/markers')
        .then(response => response.json())
        .then(data => {
            markers = data;
            renderMarkers();
            console.log('加载了', markers.length, '个标记'); // 调试日志
        })
        .catch(error => console.error('加载标记失败:', error));
}

// 渲染所有标记
function renderMarkers() {
    // 清除地图上所有标记
    map.clearMap();

    // 添加每个标记到地图
    markers.forEach(markerData => {
        // 创建圆形标记
        const circle = new AMap.Circle({
            center: new AMap.LngLat(markerData.position.lng, markerData.position.lat),
            radius: markerData.radius || 50,
            fillColor: '#3498db',
            fillOpacity: 0.3,
            strokeColor: '#2980b9',
            strokeWeight: 2,
            strokeOpacity: 0.8,
            extData: {
                id: markerData.id,
                note: markerData.note || '',
                images: markerData.images || []
            }
        });

        map.add(circle);

        // 添加鼠标事件
        circle.on('rightclick', (e) => {
            e.originEvent.stopPropagation();
            showContextMenu(e.originEvent.clientX, e.originEvent.clientY, circle);
        });

        // 添加注释文字
        if (markerData.note) {
            addLabelToCircle(circle, markerData.note);
        }

        // 如果有图片，添加图片查看按钮
        if (markerData.images && markerData.images.length > 0) {
            addImageButtonToCircle(circle);
        }

        // 如果处于编辑模式，添加可拖拽功能
        if (currentMode === 'edit') {
            makeCircleDraggable(circle);
        }
    });
}

// 添加文字标签到圆形标记
function addLabelToCircle(circle, text) {
    const center = circle.getCenter();

    // 创建文字标签对象
    const labelDiv = document.createElement('div');
    labelDiv.className = 'marker-label';
    labelDiv.textContent = text;

    const labelMarker = new AMap.Marker({
        position: center,
        content: labelDiv,
        zIndex: 10,
        anchor: 'center',
        offset: new AMap.Pixel(0, -circle.getRadius() - 10)
    });

    // 将标记绑定到Circle的extData
    const extData = circle.getExtData() || {};
    extData.labelMarker = labelMarker;
    circle.setExtData(extData);

    map.add(labelMarker);

    // 如果圆形移动，标签也跟着移动
    circle.on('moving', (e) => {
        labelMarker.setPosition(circle.getCenter());
    });

    circle.on('movend', (e) => {
        labelMarker.setPosition(circle.getCenter());
        // 更新数据
        updateMarkerPosition(circle);
    });
}

// 添加图片按钮到圆形标记
function addImageButtonToCircle(circle) {
    const center = circle.getCenter();

    // 创建图片按钮
    const imgBtnDiv = document.createElement('div');
    imgBtnDiv.className = 'marker-image-btn';
    imgBtnDiv.innerHTML = '<i>📷</i>';

    const imgBtnMarker = new AMap.Marker({
        position: center,
        content: imgBtnDiv,
        zIndex: 9,
        anchor: 'center',
        offset: new AMap.Pixel(circle.getRadius() / 2, 0)
    });

    // 将按钮绑定到Circle的extData
    const extData = circle.getExtData() || {};
    extData.imgBtnMarker = imgBtnMarker;
    circle.setExtData(extData);

    map.add(imgBtnMarker);

    // 如果圆形移动，按钮也跟着移动
    circle.on('moving', (e) => {
        const newCenter = circle.getCenter();
        imgBtnMarker.setPosition(newCenter);
        imgBtnMarker.setOffset(new AMap.Pixel(circle.getRadius() / 2, 0));
    });

    circle.on('movend', (e) => {
        const newCenter = circle.getCenter();
        imgBtnMarker.setPosition(newCenter);
        imgBtnMarker.setOffset(new AMap.Pixel(circle.getRadius() / 2, 0));
    });

    // 点击图片按钮显示预览
    imgBtnDiv.addEventListener('click', (e) => {
        e.stopPropagation();
        const markerId = extData.id;
        const markerData = markers.find(m => m.id === markerId);
        if (markerData && markerData.images && markerData.images.length > 0) {
            showImagePreview(markerData.images);
        }
    });
}

// 显示图片预览
function showImagePreview(images) {
    const container = document.getElementById('image-preview-container');
    const content = document.getElementById('image-preview-content');
    content.innerHTML = '';

    images.forEach(image => {
        const img = document.createElement('img');
        img.className = 'preview-image';
        img.src = `/static/uploads/${image.filename}`;
        img.alt = image.originalName || '图片';
        content.appendChild(img);
    });

    container.style.display = 'block';
}

// 关闭图片预览
function closeImagePreview() {
    document.getElementById('image-preview-container').style.display = 'none';
}

// 切换到添加标记模式 - 修改后的版本
function toggleAddMode() {
    // 如果已经在添加模式，则关闭
    if (currentMode === 'add') {
        resetModes();
        // 如果有点击监听器，移除它
        if (clickListener) {
            map.off('click', clickListener);
            clickListener = null;
            console.log('关闭添加标记模式，移除点击监听器'); // 调试日志
        }
        return;
    }

    // 否则进入添加模式
    resetModes();
    currentMode = 'add';
    document.getElementById('add-marker-btn').classList.add('active');

    console.log('进入添加标记模式'); // 调试日志

    // 移除可能存在的旧监听器
    if (clickListener) {
        map.off('click', clickListener);
    }

    // 添加新的点击监听器
    clickListener = function(e) {
        console.log('地图点击事件触发，当前模式:', currentMode); // 调试日志
        if (currentMode === 'add') {
            addMarker(e.lnglat);
        }
    };

    map.on('click', clickListener);
    console.log('已添加地图点击监听器'); // 调试日志
}

// 切换到编辑标记模式
function toggleEditMode() {
    resetModes();
    currentMode = currentMode === 'edit' ? 'view' : 'edit';
    document.getElementById('edit-markers-btn').classList.toggle('active', currentMode === 'edit');

    // 如果进入编辑模式，为所有标记添加可拖拽功能
    if (currentMode === 'edit') {
        makeAllCirclesDraggable();
    }
}

// 切换到删除标记模式
function toggleDeleteMode() {
    resetModes();
    currentMode = currentMode === 'delete' ? 'view' : 'delete';
    document.getElementById('delete-markers-btn').classList.toggle('active', currentMode === 'delete');
}

// 重置所有模式
function resetModes() {
    currentMode = 'view';
    document.getElementById('add-marker-btn').classList.remove('active');
    document.getElementById('edit-markers-btn').classList.remove('active');
    document.getElementById('delete-markers-btn').classList.remove('active');

    // 如果有正在编辑的圆，关闭编辑
    if (activeCircleEditor) {
        activeCircleEditor.close();
        activeCircleEditor = null;
    }
}

// 添加新标记 - 增加调试日志
function addMarker(lnglat) {
    console.log('添加标记:', lnglat.getLng(), lnglat.getLat());

    const newMarker = {
        position: {
            lng: lnglat.getLng(),
            lat: lnglat.getLat()
        },
        radius: 50,
        note: ''
    };

    fetch('/api/markers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newMarker)
    })
    .then(response => {
        if (!response.ok) {
            // 打印完整的响应信息
            console.error("HTTP 错误:", response.status, response.statusText, response);
            throw new Error(`HTTP 错误! 状态码: ${response.status}, 文本: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('标记保存成功:', data);

        // 确认后端返回的是一个对象，且包含必要的信息
        if (typeof data === 'object' && data !== null && data.id && data.position) {
            markers.push(data); //push数据
            renderMarkers(); //渲染
            // 创建 Circle
            const circle = new AMap.Circle({
                center: lnglat,
                radius: 50,
                fillColor: '#3498db',
                fillOpacity: 0.3,
                strokeColor: '#2980b9',
                strokeWeight: 2,
                strokeOpacity: 0.8,
                extData: {
                    id: data.id,
                }
            });

            map.add(circle);
            openEditDialog(circle);
        } else {
            console.error("后端返回的数据格式不正确:", data);
        }

    })
    .catch(error => {
        console.error('添加标记失败:', error);
        markers = [];
        renderMarkers(); //重新渲染，保证视图与数据同步
    });
}



// 使所有圆形可拖拽
function makeAllCirclesDraggable() {
    map.getAllOverlays('circle').forEach(circle => {
        makeCircleDraggable(circle);
    });
}

// 使圆形可拖拽
function makeCircleDraggable(circle) {
    // 创建编辑器
    AMap.plugin('AMap.CircleEditor', function() {
        const circleEditor = new AMap.CircleEditor(map, circle);

        circle.on('click', function() {
            if (currentMode === 'edit') {
                // 如果已有其他正在编辑的圆，先关闭
                if (activeCircleEditor && activeCircleEditor !== circleEditor) {
                    activeCircleEditor.close();
                }

                circleEditor.open();
                activeCircleEditor = circleEditor;

                // 修改完成时更新数据
                circleEditor.on('end', function() {
                    updateMarkerRadius(circle);
                });
            } else if (currentMode === 'delete') {
                deleteMarker(circle);
            }
        });

        // 设置可拖拽
        circle.setDraggable(true);

        // 拖拽结束后更新数据
        circle.on('dragging', function(e) {
            // 如果有标签和图片按钮，更新它们的位置
            const extData = circle.getExtData();
            if (extData.labelMarker) {
                extData.labelMarker.setPosition(circle.getCenter());
                extData.labelMarker.setOffset(new AMap.Pixel(0, -circle.getRadius() - 10));
            }

            if (extData.imgBtnMarker) {
                extData.imgBtnMarker.setPosition(circle.getCenter());
                extData.imgBtnMarker.setOffset(new AMap.Pixel(circle.getRadius() / 2, 0));
            }
        });

        circle.on('dragend', function() {
            updateMarkerPosition(circle);
        });
    });
}

// 显示右键菜单
function showContextMenu(x, y, circle) {
    selectedMarker = circle;

    const menu = document.getElementById('marker-context-menu');
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';
    menu.style.display = 'block';
}

// 编辑选中的标记
function editSelectedMarker() {
    if (selectedMarker) {
        openEditDialog(selectedMarker);
    }
    document.getElementById('marker-context-menu').style.display = 'none';
}

// 删除选中的标记
function deleteSelectedMarker() {
    if (selectedMarker) {
        deleteMarker(selectedMarker);
    }
    document.getElementById('marker-context-menu').style.display = 'none';
}

// 删除标记
function deleteMarker(circle) {
    const markerId = circle.getExtData().id;

    fetch(`/api/markers/${markerId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        // 更新本地数据
        markers = markers.filter(m => m.id !== markerId);

        // 从地图中移除标记
        map.remove(circle);

        // 移除关联的标签和按钮
        const extData = circle.getExtData();
        if (extData.labelMarker) {
            map.remove(extData.labelMarker);
        }
        if (extData.imgBtnMarker) {
            map.remove(extData.imgBtnMarker);
        }
    })
    .catch(error => console.error('删除标记失败:', error));
}

// 打开编辑标记对话框
function openEditDialog(circle) {
    const markerId = circle.getExtData().id;
    const markerData = markers.find(m => m.id === markerId);

    if (markerData) {
        // 设置当前编辑的标记
        selectedMarker = circle;

        // 设置表单值
        document.getElementById('marker-note').value = markerData.note || '';

        // 显示已有的图片
        const uploadedImagesContainer = document.getElementById('uploaded-images');
        uploadedImagesContainer.innerHTML = '';

        if (markerData.images && markerData.images.length > 0) {
            markerData.images.forEach(image => {
                const container = document.createElement('div');
                container.className = 'image-thumbnail-container';

                const img = document.createElement('img');
                img.className = 'image-thumbnail';
                img.src = `/static/uploads/${image.filename}`;
                img.alt = image.originalName || '';
                container.appendChild(img);

                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'delete-image';
                deleteBtn.textContent = 'x';
                deleteBtn.onclick = function() {
                    deleteImage(markerId, image.id, container);
                };
                container.appendChild(deleteBtn);

                uploadedImagesContainer.appendChild(container);
            });
        }

        // 显示对话框
        document.getElementById('edit-marker-dialog').style.display = 'block';
    }
}

// 关闭编辑对话框
function closeEditDialog() {
    document.getElementById('edit-marker-dialog').style.display = 'none';
    document.getElementById('image-upload').value = '';
    selectedMarker = null;
}

// 保存标记修改
function saveMarkerChanges() {
    if (!selectedMarker) return;

    const markerId = selectedMarker.getExtData().id;
    const markerData = markers.find(m => m.id === markerId);

    if (markerData) {
        const newNote = document.getElementById('marker-note').value;

        // 更新数据
        markerData.note = newNote;

        fetch(`/api/markers/${markerId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(markerData)
        })
        .then(response => response.json())
        .then(data => {
            // 更新标记显示
            const extData = selectedMarker.getExtData();
            extData.note = newNote;
            selectedMarker.setExtData(extData);

            // 更新标签
            if (extData.labelMarker) {
                map.remove(extData.labelMarker);
            }

            if (newNote) {
                addLabelToCircle(selectedMarker, newNote);
            }

            // 如果有图片，添加或更新图片按钮
            if (markerData.images && markerData.images.length > 0) {
                if (!extData.imgBtnMarker) {
                    addImageButtonToCircle(selectedMarker);
                }
            }

            closeEditDialog();
        })
        .catch(error => console.error('更新标记失败:', error));
    }
}

// 上传图片
function uploadImages() {
    if (!selectedMarker) return;

    const markerId = selectedMarker.getExtData().id;
    const fileInput = document.getElementById('image-upload');

    if (fileInput.files.length === 0) return;

    const formData = new FormData();

    // 为每个选择的文件创建上传请求
    Array.from(fileInput.files).forEach(file => {
        const formData = new FormData();
        formData.append('image', file);

        fetch(`/api/markers/${markerId}/images`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(imageData => {
            // 更新本地数据
            const markerData = markers.find(m => m.id === markerId);
            if (!markerData.images) {
                markerData.images = [];
            }
            markerData.images.push(imageData);

            // 添加图片缩略图到对话框
            const container = document.createElement('div');
            container.className = 'image-thumbnail-container';

            const img = document.createElement('img');
            img.className = 'image-thumbnail';
            img.src = `/static/uploads/${imageData.filename}`;
            img.alt = imageData.originalName || '';
            container.appendChild(img);

            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'delete-image';
            deleteBtn.textContent = 'x';
            deleteBtn.onclick = function() {
                deleteImage(markerId, imageData.id, container);
            };
            container.appendChild(deleteBtn);

            document.getElementById('uploaded-images').appendChild(container);

            // 如果没有图片按钮，添加一个
            const extData = selectedMarker.getExtData();
            if (!extData.imgBtnMarker) {
                addImageButtonToCircle(selectedMarker);
            }
        })
        .catch(error => console.error('上传图片失败:', error));
    });

    // 清空文件输入框
    fileInput.value = '';
}

// 删除图片
function deleteImage(markerId, imageId, container) {
    fetch(`/api/markers/${markerId}/images/${imageId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        // 从DOM中移除缩略图
        if (container) {
            container.remove();
        }

        // 更新本地数据
        const markerData = markers.find(m => m.id === markerId);
        if (markerData && markerData.images) {
            markerData.images = markerData.images.filter(img => img.id !== imageId);

            // 如果没有更多图片，移除图片按钮
            if (markerData.images.length === 0 && selectedMarker) {
                const extData = selectedMarker.getExtData();
                if (extData.imgBtnMarker) {
                    map.remove(extData.imgBtnMarker);
                    extData.imgBtnMarker = null;
                    selectedMarker.setExtData(extData);
                }
            }
        }
    })
    .catch(error => console.error('删除图片失败:', error));
}

// 更新标记位置
function updateMarkerPosition(circle) {
    const markerId = circle.getExtData().id;
    const center = circle.getCenter();

    const markerData = markers.find(m => m.id === markerId);

    if (markerData) {
        markerData.position = {
            lng: center.getLng(),
            lat: center.getLat()
        };

        fetch(`/api/markers/${markerId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(markerData)
        })
        .then(response => response.json())
        .catch(error => console.error('更新标记位置失败:', error));
    }
}

// 更新标记半径
function updateMarkerRadius(circle) {
    const markerId = circle.getExtData().id;
    const radius = circle.getRadius();

    const markerData = markers.find(m => m.id === markerId);

    if (markerData) {
        markerData.radius = radius;

        fetch(`/api/markers/${markerId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(markerData)
        })
        .then(response => response.json())
        .then(data => {
            // 如果有标签，更新标签位置
            const extData = circle.getExtData();
            if (extData.labelMarker) {
                extData.labelMarker.setOffset(new AMap.Pixel(0, -radius - 10));
            }

            // 如果有图片按钮，更新按钮位置
            if (extData.imgBtnMarker) {
                extData.imgBtnMarker.setOffset(new AMap.Pixel(radius / 2, 0));
            }
        })
        .catch(error => console.error('更新标记半径失败:', error));
    }
}

// 页面加载完成后初始化地图
document.addEventListener('DOMContentLoaded', initMap);
