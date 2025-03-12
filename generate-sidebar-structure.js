const fs = require('fs');
const path = require('path');

/**
 * 获取指定目录的递归文件结构
 * @param {string} dirPath - 目录路径
 * @param {string} rootDir - 根目录路径（用于计算相对路径）
 * @returns {Object} - 文件结构对象
 */
function getDirectoryStructure(dirPath, rootDir) {
    const relativePath = path.relative(rootDir, dirPath);
    const name = path.basename(dirPath);

    // 检查是否为目录
    const stats = fs.statSync(dirPath);
    if (!stats.isDirectory()) {
        return {
            name: name,
            type: 'file',
            path: relativePath.replace(/\\/g, '/')
        };
    }

    // 处理目录
    const children = [];
    const files = fs.readdirSync(dirPath);

    for (const file of files) {
        // 跳过隐藏文件
        if (file.startsWith('.')) continue;

        const filePath = path.join(dirPath, file);
        const fileStats = fs.statSync(filePath);

        if (fileStats.isDirectory()) {
            children.push(getDirectoryStructure(filePath, rootDir));
        } else {
            // 只包含markdown文件
            if (file.toLowerCase().endsWith('.md')) {
                children.push({
                    name: file,
                    type: 'file',
                    path: path.relative(rootDir, filePath).replace(/\\/g, '/')
                });
            }
        }
    }

    return {
        name: name,
        type: 'folder',
        path: relativePath.replace(/\\/g, '/') || name,
        children: children
    };
}

/**
 * 生成多个文件夹结构并合并到一个JSON文件中
 * @param {Array<string>} folders - 要扫描的文件夹名称数组
 */
function generateFoldersStructure(folders = ['wiki', 'post']) {
    const rootDir = path.resolve(__dirname); // 当前目录
    const structure = {
        name: 'root',
        type: 'folder',
        path: '',
        children: []
    };

    try {
        // 处理每个指定的文件夹
        folders.forEach(folder => {
            const folderPath = path.join(rootDir, folder);

            if (!fs.existsSync(folderPath)) {
                console.warn(`警告: ${folder} 目录不存在！将被跳过`);
                return;
            }

            // 获取文件夹结构并添加到根结构
            const folderStructure = getDirectoryStructure(folderPath, rootDir);
            structure.children.push(folderStructure);
        });

        if (structure.children.length === 0) {
            console.error('错误: 没有找到有效的文件夹！');
            return;
        }

        // 输出JSON文件
        const outputPath = path.join(rootDir, 'content-structure.json');
        fs.writeFileSync(outputPath, JSON.stringify(structure, null, 2));
        console.log(`文件结构已保存至: ${outputPath}`);

    } catch (error) {
        console.error('生成文件结构时出错:', error);
    }
}

// 执行主函数 - 可以指定要扫描的文件夹数组
generateFoldersStructure(['post', 'wiki']);