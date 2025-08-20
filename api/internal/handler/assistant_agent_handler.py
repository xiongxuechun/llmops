#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/12/3 9:22
@Author  : thezehui@gmail.com
@File    : assistant_agent_handler.py
"""
from dataclasses import dataclass
from uuid import UUID

from flask import request
from flask_login import login_required, current_user
from injector import inject

from internal.schema.assistant_agent_schema import (
    AssistantAgentChat,
    GetAssistantAgentMessagesWithPageReq,
    GetAssistantAgentMessagesWithPageResp,
)
from internal.service import AssistantAgentService
from pkg.paginator import PageModel
from pkg.response import validate_error_json, compact_generate_response, success_json, success_message


@inject
@dataclass
class AssistantAgentHandler:
    """辅助智能体处理器"""
    assistant_agent_service: AssistantAgentService

    @login_required
    def assistant_agent_chat(self):
        """与辅助智能体进行对话聊天"""
        # 1.提取请求数据并校验
        req = AssistantAgentChat()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务创建会话响应
        response = self.assistant_agent_service.chat(req, current_user)

        return compact_generate_response(response)

    @login_required
    def stop_assistant_agent_chat(self, task_id: UUID):
        """停止与辅助智能体的对话聊天"""
        self.assistant_agent_service.stop_chat(task_id, current_user)
        return success_message("停止辅助Agent会话成功")

    @login_required
    def get_assistant_agent_messages_with_page(self):
        """获取与辅助智能体的消息分页列表"""
        # 1.提取请求并校验数据
        req = GetAssistantAgentMessagesWithPageReq(request.args)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务获取数据
        messages, paginator = self.assistant_agent_service.get_conversation_messages_with_page(
            req, current_user
        )

        # 3.创建响应数据结构
        resp = GetAssistantAgentMessagesWithPageResp(many=True)

        return success_json(PageModel(list=resp.dump(messages), paginator=paginator))

    @login_required
    def delete_assistant_agent_conversation(self):
        """清空/删除与辅助智能体的聊天会话记录"""
        # 1.调用服务清空辅助Agent会话列表
        self.assistant_agent_service.delete_conversation(current_user)

        # 2.清空成功后返回消息响应
        return success_message("清空辅助Agent会话成功")
