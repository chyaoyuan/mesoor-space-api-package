"""
MesoorSpace API 异常类定义
"""
from typing import Optional, Dict, Any


class MesoorSpaceException(Exception):
    """MesoorSpace API 异常类"""
    
    def __init__(
        self, 
        message: str, 
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
        request_data: Optional[Dict[str, Any]] = None
    ):
        """
        初始化异常
        
        Args:
            message: 错误消息
            status_code: HTTP状态码
            response_data: 响应数据
            request_data: 请求数据（敏感信息会被过滤）
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data

    def __str__(self) -> str:
        """返回格式化的错误信息"""
        parts = [self.message]
        
        if self.status_code:
            parts.append(f"Status Code: {self.status_code}")
        
        if self.response_data:
            parts.append(f"Response: {self.response_data}")
            
        return " | ".join(parts)
