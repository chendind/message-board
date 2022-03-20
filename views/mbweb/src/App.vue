<template>
  <div id="app">
    <header class="mb-header">
      <div class="mb-header__user" style="cursor: pointer;">
        <template v-if="user">
          <van-popover v-model="showUserMemu" :actions="userMemuActions" @select="onSelectUserMemuActions">
            <template #reference>
              <div @click="showUserMemu = !showUserMemu">
                <van-icon name="user-o" /> {{user.username}}[{{user.email}}]
              </div>
            </template>
          </van-popover>
        </template>
        <template v-else>
          <van-button round size="small" type="primary" style="margin-right: 15px;" @click="$store.commit('app/setSignInDialogShow', true)">登录</van-button>
          <van-button round size="small" @click="$store.commit('app/setSignUpDialogShow', true)">注册</van-button>
        </template>
      </div>
    </header>
    <section>
      <van-cell-group inset>
        <van-field
          v-model="message"
          rows="2"
          autosize
          label="留言"
          type="textarea"
          maxlength="200"
          placeholder="请输入留言"
          show-word-limit
        />
      </van-cell-group>
      <div style="padding: 10px 15px;">
        <van-button round block type="warning" color="#0099FF" @click="postTopComment">提交留言</van-button>
      </div>
    </section>
    <section style="padding: 15px;">
      <div class="mb-comment-title">
        留言板
      </div>
      <div style="">
        <comment-list :comments="comments" v-if="comments.length > 0"></comment-list>
        <div class="mb-comment" v-else-if="loading" style="padding: 30px 0;">
          <van-skeleton title avatar :row="3"></van-skeleton>
        </div>
        <div class="mb-comment" v-else>
          <van-empty description="Wow~这里好安静哦，快来po第一条留言吧"></van-empty>
        </div>
      </div>
    </section>
    <van-dialog class="sign-in-dialog" :value="signInDialogShow" title="登录" :showConfirmButton="false">
      <div style="position: absolute;right: 15px;top: 28px;font-size: 16px;cursor: pointer;" @click="$store.commit('app/setSignInDialogShow', false)">
        <van-icon name="cross" />
      </div>
      <div class="sign-in-dialog__tips">您还未登录，登录后可留言或回复</div>
      <div style="margin-top: 15px">
        <van-cell-group>
          <van-field v-model="account" label="账号" placeholder="请输入用户名或邮箱" autofocus />
          <van-field v-model="password" type="password" label="密码" placeholder="请输入密码" />
        </van-cell-group>
        <div style="padding-left: 15px;margin-top: 15px;font-size: 14px;color: #646566;user-select:none;">
          <label for="remember" style="cursor: pointer;">
            <input id="remember" type="checkbox" v-model="remember" style="cursor: pointer;">
            记住我
          </label>
        </div>
      </div>
      <div style="margin-top: 15px;padding: 0 15px;">
        <van-button round block type="primary" @click="signIn">登录</van-button>
      </div>
      <div style="margin-top: 15px;color: #666;font-size: 12px;text-align: center;padding-bottom: 30px;">
        还没有账号？<span @click="$store.commit('app/setSignUpDialogShow', true)" class="signUpText">立即注册</span>
      </div>
    </van-dialog>
    <van-dialog class="sign-up-dialog" :value="signUpDialogShow" title="注册" :showConfirmButton="false">
      <div style="position: absolute;right: 15px;top: 28px;font-size: 16px;" @click="$store.commit('app/setSignUpDialogShow', false)">
        <van-icon name="cross" />
      </div>
      <div style="margin-top: 15px">
        <van-cell-group>
          <van-field v-model="signUpUsername" label="用户名" placeholder="请输入5~20位用户名" autofocus />
          <van-field v-model="signUpEmail" label="邮箱" placeholder="请输入邮箱" />
          <van-field v-model="signUpPassword" type="password" label="密码" placeholder="请输入8~20位密码" />
        </van-cell-group>
        <div style="font-size: 12px;color: #999;padding: 5px 15px;">
          <div>tips: </div>
          <div>1.用户名只能使用字母和数字，长度在5~20之间</div>
          <div>2.密码长度在8~20之间，至少包含一个大写、一个小写、一个数字、一个特殊符号</div>
        </div>
      </div>
      <div style="margin-top: 15px;padding: 0 15px;">
        <van-button round block type="primary" @click="signUp">注册</van-button>
      </div>
      <div style="margin-top: 15px;color: #666;font-size: 12px;text-align: center;padding-bottom: 30px;">
        已有账号？<span @click="$store.commit('app/setSignInDialogShow', true)" class="signUpText">立即登录</span>
      </div>
    </van-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { postComment } from '@/api'
import commentList from '@/components/commentList'
export default {
  name: 'App',
  components: {
    commentList
  },
  data() {
    return {
      loading: true,
      showUserMemu: false,
      userMemuActions: [
        { text: '退出登录' }
      ],
      message: '',
      account: '',
      password: '',
      remember: false,
      signUpUsername: '',
      signUpEmail: '',
      signUpPassword: ''
    }
  },
  computed: {
    ...mapState({
      user: state => state.app.user,
      signInDialogShow: state => state.app.signInDialogShow,
      signUpDialogShow: state => state.app.signUpDialogShow,
      comments: state => state.app.comments,
    })
  },
  methods: {
    getItemIndexBeyItemKey (list, key, keyName) {
      for (let i in list) {
        if (list[i][keyName] === key) {
          return i
        }
      }
      return null
    },
    signIn() {
      this.$store.dispatch('app/signIn', {
        username: this.account,
        email: this.account,
        password: this.password,
        remember: this.remember ? 1 : 0
      }).then(() => {
        this.account = ''
        this.password = ''
        this.remember = false
      }).catch(res => {})
    },
    signUp() {
      this.$store.dispatch('app/signUp', {
        username: this.signUpUsername,
        email: this.signUpEmail,
        password: this.signUpPassword
      }).then(() => {
        this.signUpUsername = ''
        this.signUpEmail = ''
        this.signUpPassword = ''
      }).catch(res => {})
    },
    postTopComment() {
      if (!this.user) {
        this.$store.commit('app/setSignInDialogShow', true)
      } else {
        postComment({
          content: this.message
        }).then(res => {
          this.message = ''
          this.$store.dispatch('app/getComments')
        }).catch(res => {})
      }
    },
    onSelectUserMemuActions() {
      this.$store.dispatch('app/signOut').catch(res => {})
    }
  },
  created() {
    this.$store.dispatch('app/getSelf').catch(res => {})
    Promise.all([this.$store.dispatch('app/getComments'), new Promise(resolve => {
      setTimeout(() => {
        resolve()
      }, 1500)
    })]).then(() => {
      this.loading = false
    })
  }
}
</script>

<style>
#app {
  
}
</style>
