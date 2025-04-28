"""URL处理工具函数"""

def get_static_url(path: str, settings) -> str:
    """生成静态资源的完整URL

    Args:
        path: 资源相对路径
        settings: 应用配置

    Returns:
        完整的静态资源URL
    """
    if path.startswith('/'):
        path = path[1:]
    return f"{settings.BASE_URL}{settings.STATIC_PATH}/{path}"