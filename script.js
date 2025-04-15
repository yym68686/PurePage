import { processMathAndMarkdown, renderMathInElement } from './htmd/latex.js';
document.addEventListener('DOMContentLoaded', function() {
    // 元素获取
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const togglePin = document.getElementById('togglePin');
    const fileTree = document.getElementById('fileTree');
    const markdownContent = document.getElementById('markdown-content');
    const currentFileName = document.getElementById('currentFileName');
    const sidebarTitle = document.querySelector('.sidebar-header h3');

    // 侧边栏状态
    let isPinned = false;

    // 检查URL并加载对应内容
    checkUrlAndLoadContent();

    // 修改：检测是否为移动设备
    const isMobile = () => window.innerWidth <= 768;

    // 修改：初始化时根据设备类型设置侧边栏状态
    if (isMobile()) {
        sidebar.classList.add('collapsed');
    }

    // 修改：切换侧边栏可见性的处理
    sidebarToggle.addEventListener('click', function() {
        if (isMobile()) {
            sidebar.classList.toggle('expanded');
        } else {
            sidebar.classList.toggle('collapsed');
        }
    });

    // 修改：切换固定状态的处理
    togglePin.addEventListener('click', function() {
        if (isMobile()) {
            // 在移动端，点击 pin 按钮直接关闭侧边栏
            sidebar.classList.remove('expanded');
        } else {
            isPinned = !isPinned;
            togglePin.classList.toggle('pinned', isPinned);
            if (!isPinned) {
                sidebar.classList.add('collapsed');
            }
        }
    });

    // 当鼠标离开侧边栏且未固定时，折叠侧边栏
    sidebar.addEventListener('mouseleave', function() {
        if (!isPinned) {
            sidebar.classList.add('collapsed');
        }
    });

    // 当鼠标进入侧边栏切换按钮时，展开侧边栏
    sidebarToggle.addEventListener('mouseenter', function() {
        sidebar.classList.remove('collapsed');
    });

    // 修改：将事件监听器添加到标题文本元素上
    sidebarTitle.addEventListener('click', function() {
        // 加载首页内容
        loadFileContent('index.md');
        // 更新URL
        updateUrl('index.md');
        // 清除所有文件的活动状态
        document.querySelectorAll('.file-tree-item').forEach(item => {
            item.classList.remove('active');
        });

        // 添加：在移动端自动隐藏侧边栏
        if (isMobile()) {
            sidebar.classList.remove('expanded');
        }
    });

    // 根据URL加载内容
    function checkUrlAndLoadContent() {
        // 获取URL中的路径
        let path = window.location.hash.substring(1);

        // 如果URL没有指定路径，则加载默认文件
        if (!path) {
            loadFileContent('index.md');
            return;
        }

        // 使用URL中的路径加载内容
        loadFileContent(path);
    }

    // 更新URL而不刷新页面
    function updateUrl(filePath) {
        // 使用hash方式更新URL
        window.location.hash = filePath;
    }

    // 修改加载文件树的函数，使用预生成的JSON文件
    async function loadFileTree() {
        try {
            // 使用fetch加载预生成的JSON文件 - 更改为新的文件名
            const response = await fetch('content-structure.json');
            if (!response.ok) {
                throw new Error(`加载文件结构失败: HTTP ${response.status}`);
            }

            const fileStructure = await response.json();
            fileTree.innerHTML = generateFileTree(fileStructure);

            // 默认展开第一级文件夹
            document.querySelectorAll('.file-tree-folder').forEach(folder => {
                // 只展开第一级
                if (folder.parentElement.id === 'fileTree') {
                    folder.classList.add('expanded');
                }
            });

            // 为文件夹添加点击事件
            document.querySelectorAll('.file-tree-folder > .file-tree-item').forEach(folder => {
                folder.addEventListener('click', function(e) {
                    e.stopPropagation();
                    this.parentElement.classList.toggle('expanded');
                });
            });

            // 为文件添加点击事件
            document.querySelectorAll('.file-tree-item.file').forEach(file => {
                file.addEventListener('click', function() {
                    // 移除所有文件的活动状态
                    document.querySelectorAll('.file-tree-item').forEach(item => {
                        item.classList.remove('active');
                    });

                    // 添加当前文件的活动状态
                    this.classList.add('active');

                    // 获取文件路径并加载内容
                    const filePath = this.getAttribute('data-path');
                    loadFileContent(filePath);

                    // 更新URL
                    updateUrl(filePath);

                    // 更新当前文件名显示 (如果有此元素)
                    if (currentFileName) {
                        currentFileName.textContent = this.textContent.trim();
                    }

                    // 在移动端自动隐藏侧边栏
                    if (isMobile()) {
                        sidebar.classList.remove('expanded');
                    }
                });
            });

            // 如果URL中有文件路径，突出显示对应的文件
            highlightActiveFile();
        } catch (error) {
            fileTree.innerHTML = `<div class="error">加载文件失败: ${error.message}</div>`;
            console.error('加载文件结构失败:', error);
        }
    }

    // 根据当前URL突出显示活动文件
    function highlightActiveFile() {
        let path = window.location.hash.substring(1);
        if (!path) return;

        // 查找对应的文件元素并激活
        const fileElement = document.querySelector(`.file-tree-item.file[data-path="${path}"]`);
        if (fileElement) {
            // 清除其他活动状态
            document.querySelectorAll('.file-tree-item').forEach(item => {
                item.classList.remove('active');
            });

            // 添加活动状态
            fileElement.classList.add('active');

            // 展开父文件夹
            let parent = fileElement.parentElement;
            while (parent && parent.classList.contains('file-tree-folder-content')) {
                parent.parentElement.classList.add('expanded');
                parent = parent.parentElement.parentElement;
            }
        }
    }

    // 生成文件树HTML - 根节点隐藏处理
    function generateFileTree(item, level = 0) {
        let html = '';

        // 根节点特殊处理 - 直接显示子项而不显示根节点本身
        if (item.name === 'root' && level === 0) {
            if (item.children && item.children.length) {
                item.children.forEach(child => {
                    html += generateFileTree(child, level);
                });
            }
            return html;
        }

        // 常规文件夹和文件处理
        if (item.type === 'folder') {
            html += `<div class="file-tree-folder${level === 0 ? ' root-folder' : ''}" data-path="${item.path}">
                      <div class="file-tree-item" style="padding-left: ${15 + level * 10}px">
                        ${item.name}
                      </div>
                      <div class="file-tree-folder-content">`;

            if (item.children && item.children.length) {
                item.children.forEach(child => {
                    html += generateFileTree(child, level + 1);
                });
            }

            html += `</div>
                   </div>`;
        } else if (item.type === 'file') {
            html += `<div class="file-tree-item file" data-path="${item.path}" style="padding-left: ${15 + level * 10}px">
                      ${item.name}
                    </div>`;
        }
        return html;
    }

    // 加载文件内容
    async function loadFileContent(filePath) {
        try {
            markdownContent.innerHTML = '<div class="loading">加载内容中...</div>';

            // 修改fetchFileContent函数来加载实际的Markdown文件
            const content = await fetchFileContent(filePath);

            // 使用用户提供的Markdown渲染函数处理内容
            const renderedContent = processMathAndMarkdown(content);
            markdownContent.innerHTML = renderedContent;
            await renderMathInElement(markdownContent);
        } catch (error) {
            markdownContent.innerHTML = `<div class="error">加载内容失败: ${error.message}</div>`;
        }
    }

    // 修改fetchFileContent函数来加载实际的Markdown文件
    async function fetchFileContent(filePath) {
        try {
            // 直接从相对路径加载markdown文件
            const response = await fetch(filePath);
            if (!response.ok) {
                throw new Error(`加载文件失败: HTTP ${response.status}`);
            }
            return await response.text();
        } catch (error) {
            console.error(`加载文件失败 ${filePath}:`, error);
            return `# 加载失败\n\n无法加载文件: ${filePath}\n\n错误: ${error.message}`;
        }
    }

    // 监听URL变化
    window.addEventListener('hashchange', checkUrlAndLoadContent);

    // 页面加载时初始化文件树
    loadFileTree();

    // 添加：监听窗口大小变化
    window.addEventListener('resize', function() {
        if (!isMobile()) {
            sidebar.classList.remove('expanded');
            if (!isPinned) {
                sidebar.classList.add('collapsed');
            }
        }
    });

    // 添加：点击内容区域时隐藏侧边栏
    const content = document.getElementById('content');
    content.addEventListener('click', function(e) {
        if (isMobile()) {
            // 确保点击的不是链接元素
            if (!e.target.closest('a')) {
                sidebar.classList.remove('expanded');
            }
        }
    });

    // 添加：阻止侧边栏内的点击事件冒泡到内容区域
    sidebar.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});
