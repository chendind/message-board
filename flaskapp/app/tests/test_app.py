# -*- coding: utf-8 -*-
import unittest, json
from flask import current_app
from app import create_app, db
from tests import TestConfig
from app.utils import ResponseMap

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        with self.app_context:
            db.create_all()
        self.app_context.push()
        self.client = self.app.test_client()
    
    def test_signin_without_params(self):
        # No parameters are passed when sign in
        # 登录时什么参数都不传
        response = self.client.post("/api/user/signIn", data={})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.REQUEST_PARAMS_ERROR[0])
    
    def test_signin_with_wrong_username(self):
        # Sign in with wrong username
        # 使用错误的用户名登录
        response = self.client.post("/api/user/signIn", data={'username': 'someone', 'password': 'Aa12345.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.USER_NON_EXIST[0])
    
    def test_signin_with_unregistered_email(self):
        # Sign in with unregistered email
        # 使用未注册的邮箱登录
        response = self.client.post("/api/user/signIn", data={'email': 'someone', 'password': 'Aa12345.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.USER_NON_EXIST[0])
    
    def test_signin_with_wrong_password(self):
        # Sign up in advance
        # 提前注册好用户
        self.client.post("/api/user/signUp", data={'username': 'someone', 'email': 'someone@github.com', 'password': 'Aa12345.'})
        # Sign in with wrong password
        # 使用错误的密码登录
        response = self.client.post("/api/user/signIn", data={'username': 'someone', 'password': 'wrong'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.PASSWORD_ERROR[0])
        
    def test_signup_with_less_then_5_username(self):
        # Sign up with a username of less than 5 digits
        # 注册时使用不足5位的用户名
        response = self.client.post("/api/user/signUp", data={'username': 'aaaa', 'email': 'someone@github.com', 'password': 'Aa12345.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.USERNAME_FORMAT_ERROR[0])

    def test_signup_with_more_than_20_username(self):
        # Register with a username with more than 20 digits
        # 注册时使用超过20位的用户名
        response = self.client.post("/api/user/signUp", data={'username': 'aaaaaaaaaaaaaaaaaaaaa', 'email': 'someone@github.com', 'password': 'Aa12345.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.USERNAME_FORMAT_ERROR[0])

    def test_signup_with_symbol_username(self):
        # Sign up with a username contained symbols
        # 注册时使用含符号的用户名
        response = self.client.post("/api/user/signUp", data={'username': 'Johnson^', 'email': 'someone@github.com', 'password': 'Aa12345.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.USERNAME_FORMAT_ERROR[0])

    def test_signup_with_wrong_email_format(self):
        # Sign up with a wrong email format
        # 注册时使用错误的邮箱格式
        response = self.client.post("/api/user/signUp", data={'username': 'Johnson', 'email': 'someone.github.com', 'password': 'Aa12345.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.EMAIL_FORMAT_ERROR[0])

    def test_signup_with_long_email(self):
        # Sign up with a long email
        # 注册时使用邮箱过长
        response = self.client.post("/api/user/signUp", data={'username': 'Johnson', 'email': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@github.com', 'password': 'Aa12345.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.EMAIL_FORMAT_ERROR[0])

    def test_signup_with_password_miss_capital_letter(self):
        # Sign up with a password missing capital letter
        # 注册时密码缺少大写字母
        response = self.client.post("/api/user/signUp", data={'username': 'someone', 'email': 'someone@github.com', 'password': 'a12345678.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.PASSWORD_FORMAT_ERROR[0])

    def test_signup_with_password_miss_lowercase_letter(self):
        # Sign up with a password missing lowercase letter
        # 注册时密码缺少小写字母
        response = self.client.post("/api/user/signUp", data={'username': 'someone', 'email': 'someone@github.com', 'password': 'A12345678.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.PASSWORD_FORMAT_ERROR[0])

    def test_signup_with_password_miss_number(self):
        # Sign up with a password missing number
        # 注册时密码缺少数字
        response = self.client.post("/api/user/signUp", data={'username': 'someone', 'email': 'someone@github.com', 'password': 'Aaaaaaaaa.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.PASSWORD_FORMAT_ERROR[0])

    def test_signup_with_password_miss_special_symbol(self):
        # Sign up with a password missing special symbol
        # 注册时密码缺少特殊符号
        response = self.client.post("/api/user/signUp", data={'username': 'someone', 'email': 'someone@github.com', 'password': 'Aaaaaaaaa1'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.PASSWORD_FORMAT_ERROR[0])

    def test_signup_with_less_then_8_password(self):
        # Sign up with a password of less than 8 digits
        # 注册时密码不足8位
        response = self.client.post("/api/user/signUp", data={'username': 'someone', 'email': 'someone@github.com', 'password': 'Aa1234.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.PASSWORD_FORMAT_ERROR[0])
    
    def test_signup_with_more_then_20_password(self):
        # Sign up with a password of more than 20 digits
        # 注册时密码超过20位
        response = self.client.post("/api/user/signUp", data={'username': 'someone', 'email': 'someone@github.com', 'password': 'Aa123456789101112130.'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.PASSWORD_FORMAT_ERROR[0])

    def test_signup_with_correct_username_email_password(self):
        # Sign up with a correct username and a correct email and a correct password
        # 注册时用户名、邮箱、密码均使用正确的格式
        response = self.client.post("/api/user/signUp", data={'username': 'someone', 'email': 'someone@github.com', 'password': 'Aa1234567890!@#$%^&*'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.SUCCESS[0])
    
    def test_get_comment_before_signin(self):
        # Get comments without sign in
        # 未登录直接获取留言
        response = self.client.get("/api/comment/tree")
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.SUCCESS[0])

    def test_post_comment_before_signin(self):
        # Post a comment without sign in
        # 未登录直接留言
        response = self.client.post("/api/comment", data={'content': '这是一条测试留言，并且在3个字以上200字以下'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.LOGIN_TIMEOUT[0])
    
    def test_post_comment_after_signin(self):
        # Sign up and sign in
        # 进行注册+登录
        self.client.post("/api/user/signUp", data={'username': 'someone', 'email': 'someone@github.com', 'password': 'Aa12345.'})
        self.client.post("/api/user/signIn", data={'username': 'someone', 'password': 'Aa12345.'})

        # Post a comment(less than 3 characters) after sign in
        # 登录后留言，不满3个字
        response = self.client.post("/api/comment", data={'content': '呵呵'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.MESSAGE_CONTENT_FORMAT_ERROR[0])

        # Post a comment(more than 200 characters) after sign in
        # 登录后留言，超过200个字
        response = self.client.post("/api/comment", data={'content': '200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字。'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.MESSAGE_CONTENT_FORMAT_ERROR[0])

        # Post a comment(exactly 200 characters) after sign in
        # 登录后留言，正好200字
        response = self.client.post("/api/comment", data={'content': '200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字200字'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.SUCCESS[0])

    def test_reply_comment_after_signin(self):
        # Sign up + sign in + post a comment
        # 进行注册+登录+留言
        self.client.post("/api/user/signUp", data={'username': 'someone', 'email': 'someone@github.com', 'password': 'Aa12345.'})
        self.client.post("/api/user/signIn", data={'username': 'someone', 'password': 'Aa12345.'})
        self.client.post("/api/comment", data={'content': '这是一条等待被回复的留言'})

        # Get comments after sign in
        # 登录后获得留言
        response = self.client.get("/api/comment/tree")
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.SUCCESS[0])

        # Reply a comment after sign in
        # 登录后针对某留言进行回复
        parent_comment_id = resp_dict["data"][0]['comment']['id']
        response = self.client.post("/api/comment", data={'content': '感谢您的留言！', 'parent_comment_id': parent_comment_id})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn("code", resp_dict)
        code = resp_dict.get("code")
        self.assertEqual(code, ResponseMap.SUCCESS[0])

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()