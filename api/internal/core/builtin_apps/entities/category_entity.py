#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/11/20 13:25
@Author  : thezehui@gmail.com
@File    : category_entity.py
"""
from pydantic import BaseModel, Field


class CategoryEntity(BaseModel):
    """内置工具分类实体"""
    category: str = Field(default="")  # 分类唯一标识
    name: str = Field(default="")  # 分类对应的名称
