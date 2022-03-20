# -*- coding: utf-8 -*-
from . import comment
from flask_login import login_user, logout_user, login_required, current_user
from flask import request, current_app
from app.models import User, Comment
from app.comment.service import getParentComment, addComment, getCommentsJoinWithUser
from app.utils import mkresponse, ResponseMap

# Post a message or comment
# 发布留言或评论
@comment.route('', methods = ['post'])
@login_required
def post():
    content = request.form.get('content', type = str, default = None)
    parent_comment_id = request.form.get('parent_comment_id', type = int, default = None)
    if not Comment.checkContent(content):
        return mkresponse(ResponseMap.MESSAGE_CONTENT_FORMAT_ERROR)
    ancestor_comment_id = None
    if parent_comment_id is not None:
        parent_comment = getParentComment(parent_comment_id)
        # Get the ancestor ID of the message and store it. This field will come into play if pagination is introduced in the future
        # 获得留言的祖先ID并存储。未来如果引入分页功能，该字段将发挥作用
        ancestor_comment_id = parent_comment.ancestor_comment_id or parent_comment_id
    addComment(current_user.id, content, parent_comment_id, ancestor_comment_id)
    return mkresponse(code=ResponseMap.ADD_SUCCESS)

# Get comments data(tree structure)
# 得到树形评论数据
@comment.route('/tree', methods = ['get'])
def getTree():
    # Get comment data with user data
    # 获取含用户的评论数据
    datas = getCommentsJoinWithUser()
    # Construct a structure, `children` field is used to store child nodes
    # 构造结构体，`children`用于存放子节点
    datasList = [{
        'comment': _data[0].toDict(),
        'user': _data[1].toDict(),
        'children': []
    } for _data in datas]
    # Construct a dict for get comment data directly by `comment.id`
    # 构造一个字典，用于根据comment.id快速获得评论数据
    commentIdMap = dict((_item['comment']['id'], _item) for _item in datasList)
    tree = []
    for data in datasList:
        if data['comment']['parent_comment_id'] is None:
            # Insert the top-level message to the top level of the tree structure
            # 将顶层的留言插入到树形结构的最上层
            tree.append(data)
        else:
            # Get this comment's parent
            # 取出子元素的父元素
            parentData = commentIdMap[data['comment']['parent_comment_id']]
            parentData['children'].append(data)
    return mkresponse(data = tree)