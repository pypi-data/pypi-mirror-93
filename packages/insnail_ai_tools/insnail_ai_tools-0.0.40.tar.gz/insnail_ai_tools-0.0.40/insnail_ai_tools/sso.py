import datetime
import inspect
import time
from functools import wraps

import redis
from fastapi import status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt


class Sso:
    def __init__(
        self,
        secret_key: str,
        redis_uri: str,
        expire_minutes: int = 60 * 24,
        algorithm: str = "HS256",
    ):
        self._secret_key = secret_key
        self._expire_minutes = expire_minutes
        self._algorithm = algorithm
        self._redis = redis.Redis(redis_uri)

    def generate_token(self, user_id: str) -> str:
        """
        根据用户ID生成token
        :param user_id: 用户ID
        :return: token
        """
        data = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(minutes=self._expire_minutes),
        }
        token = jwt.encode(data, self._secret_key, algorithm=self._algorithm)
        return token

    def decode_token(self, token: str) -> dict:
        """
        解码token
        :param token: 对应的token
        :return: 解码结果。exp 为过期时间
        """
        data = jwt.decode(token, self._secret_key)
        return data

    def check_expire(self, token: str) -> bool:
        """
        判断token是否过期
        :param token: 对应token
        :return: True为正常、False为过期
        """
        try:
            data = self.decode_token(token)
        except JWTError:
            return False
        if data["exp"] > time.time():
            return True
        else:
            return False

    def _add_token(self, token: str):
        """将token添加至redis"""
        self._redis.sadd("token", token)

    def _remove_token(self, token: str):
        """移除token"""
        self._redis.srem("token", token)

    def _exists_token(self, token: str) -> bool:
        """判断token是否在redis"""
        return self._redis.sismember("token", token)

    def fast_api_sso(self, func):
        def _wrapper(*args, **kwargs):
            token = kwargs.get("token")
            # token未过期
            if self._exists_token(token) and self.check_expire(token):
                return func(*args, **kwargs)
            else:
                return JSONResponse(
                    {"msg": "token不存在或已过期"}, status_code=status.HTTP_401_UNAUTHORIZED
                )

        @wraps(func)
        def wrapper(*args, **kwargs):
            return _wrapper(*args, **kwargs)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return _wrapper(*args, **kwargs)

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return wrapper

    def login(self, user_id: str) -> str:
        token = self.generate_token(user_id)
        self._add_token(token)
        return token

    def logout(self, token: str):
        self._remove_token(token)
