import sys
import json
import shutil
import time
import re
from pathlib import Path
from datetime import datetime

def download_and_process(comic_id):
    """下载漫画并处理"""
    try:
        # 记录当前目录下的所有文件夹
        before_dirs = set(d.name for d in Path(".").iterdir() if d.is_dir())
        
        # 下载漫画
        print(f"开始下载漫画 {comic_id}...")
        
        # 导入jmcomic并下载
        import jmcomic
        jmcomic.download_album(comic_id)
        
        # 等待一下，确保文件写入完成
        time.sleep(2)
        
        # 获取下载后新增的文件夹
        after_dirs = set(d.name for d in Path(".").iterdir() if d.is_dir())
        new_dirs = after_dirs - before_dirs
        
        if not new_dirs:
            print("下载完成，但找不到新增的目录")
            return False
        
        # 使用最新创建的目录
        newest_dir = max(new_dirs, key=lambda d: Path(d).stat().st_mtime)
        source_path = Path(newest_dir)
        print(f"找到下载目录: {source_path}")
        
        # 目标目录 - 前端的mock目录
        target_dir = Path("../src/assets/mock")
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 目标漫画目录
        target_path = target_dir / comic_id
        
        # 如果目标目录已存在，先删除
        if target_path.exists():
            print(f"目标目录 {target_path} 已存在，正在删除...")
            shutil.rmtree(target_path)
        
        # 创建目标目录
        target_path.mkdir(parents=True, exist_ok=True)
        
        # 复制文件而不是整个目录结构
        print(f"正在处理文件从 {source_path} 到 {target_path}...")
        
        # 获取所有图片文件
        image_files = []
        for ext in ['.jpg', '.png', '.webp']:
            image_files.extend(list(source_path.glob(f"*{ext}")))
        
        # 按文件名排序
        def extract_page_number(path):
            # 尝试从文件名中提取数字
            numbers = re.findall(r'\d+', path.stem)
            return int(numbers[0]) if numbers else 0
        
        image_files.sort(key=extract_page_number)
        
        # 直接复制所有图片到目标目录
        image_paths = []
        for i, img_file in enumerate(image_files):
            # 使用统一的命名格式
            new_name = f"{i+1:05d}{img_file.suffix}"
            shutil.copy2(img_file, target_path / new_name)
            # 添加图片路径到列表
            image_paths.append(f"/src/assets/mock/{comic_id}/{new_name}")
        
        # 获取漫画标题
        title = source_path.name
        
        # 创建漫画信息
        comic_info = {
            "id": comic_id,
            "title": title,
            "cover": image_paths[0] if image_paths else "",
            "author": "未知",
            "description": "从JM漫画下载的漫画",
            "tags": ["漫画", "JM漫画"],
            "updateTime": datetime.now().isoformat().split('T')[0],
            "status": "completed"  # 确保status字段的值是'completed'或'ongoing'
        }
        
        # 清理源目录
        if source_path.exists():
            shutil.rmtree(source_path)
        
        # 更新前端的漫画列表
        update_frontend_comics_list(comic_id, comic_info, image_paths)
        
        print(f"漫画 {comic_id} 处理完成, 已添加到前端mock数据")
        return True
    except Exception as e:
        print(f"下载或处理漫画 {comic_id} 时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_frontend_comics_list(comic_id, comic_info, image_paths):
    """更新前端的漫画列表"""
    try:
        # 前端漫画列表文件路径
        comics_list_path = Path("../src/assets/mock/comics.json")
        
        # 如果文件不存在，创建一个空列表
        if not comics_list_path.exists():
            comics_list = []
        else:
            # 读取现有的漫画列表
            with open(comics_list_path, "r", encoding="utf-8") as f:
                comics_list = json.load(f)
        
        # 检查漫画是否已存在于列表中
        comic_exists = False
        for i, comic in enumerate(comics_list):
            if comic["id"] == comic_id:
                # 更新现有漫画信息
                comics_list[i] = comic_info
                comic_exists = True
                break
        
        # 如果漫画不存在，添加到列表
        if not comic_exists:
            comics_list.append(comic_info)
        
        # 保存更新后的漫画列表
        with open(comics_list_path, "w", encoding="utf-8") as f:
            json.dump(comics_list, f, ensure_ascii=False, indent=2)
        
        # 创建章节数据
        chapter = {
            "id": f"{comic_id}-1",
            "comicId": comic_id,
            "title": "第1话",
            "order": 1,
            "updateTime": datetime.now().isoformat().split('T')[0],
            "pageCount": len(image_paths)
        }
        
        # 保存章节数据
        chapters_path = Path("../src/assets/mock/chapters.json")
        if not chapters_path.exists():
            chapters = []
        else:
            with open(chapters_path, "r", encoding="utf-8") as f:
                chapters = json.load(f)
        
        # 检查章节是否已存在
        chapter_exists = False
        for i, ch in enumerate(chapters):
            if ch["id"] == chapter["id"]:
                chapters[i] = chapter
                chapter_exists = True
                break
        
        if not chapter_exists:
            chapters.append(chapter)
        
        with open(chapters_path, "w", encoding="utf-8") as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)
        
        print(f"漫画 {comic_id} 已添加到前端漫画列表")
    except Exception as e:
        print(f"更新前端漫画列表时出错: {e}")

def main():
    # 获取命令行参数作为漫画ID，默认为416330
    comic_id = sys.argv[1] if len(sys.argv) > 1 else "416330"
    
    # 下载并处理漫画
    download_and_process(comic_id)

if __name__ == "__main__":
    main() 