<template>
  <div>
    <div v-for="(comment, index) in comments" :key="comment.comment.id" class="mb-comment" :id="`comment${comment.comment.id}`">
      <div class="mb-comment__inner" :style="{backgroundColor: highlightCommentId === comment.comment.id ? '#f8f8f8': 'transparent'}">
        <div class="mb-comment__left">
          <img class="mb-comment__avatar" src="static/images/avatar.jpg" alt="头像">
          <div class="mb-comment__username">{{comment.user.username}}</div>
        </div>
        <div class="mb-comment__right">
          <div class="mb-comment__applyto" v-if="parent"><a style="cursor: help;" @mouseenter="highlightParent" @mouseleave="removeHighlightParent" :href="`#comment${parent.comment.id}`">回复{{parent.user.username}}</a></div>
          <div class="mb-comment__content">{{comment.comment.content}}</div>
          <div class="mb-comment__time">{{comment.comment.create_time_str}}</div>
          <van-button icon="chat-o" round type="default" size="mini" @click="showReplyField(comment.comment.id)" v-if="replyFieldShowIds.indexOf(comment.comment.id) === -1">回复</van-button>
          <van-cell-group v-else>
            <van-field
              v-model="message"
              rows="2"
              autosize
              :label="'回复' + comment.user.username"
              type="textarea"
              maxlength="200"
              placeholder="请输入回复内容"
              show-word-limit
            />
            <div style="padding: 10px;">
              <van-button icon="success" round size="mini" type="default" @click="postComment(index, comment.comment.id)">提交</van-button>
              <van-button icon="cross" round size="mini" type="default" @click="hideReplyField(comment.comment.id)">取消</van-button>
            </div>
          </van-cell-group>
        </div>
      </div>
      <div :style="{paddingLeft: level === 0 ? '80px': '0px'}">
        <comment-list :comments="comment.children" :parent="comment" v-if="comment.children.length" :level="level + 1"  v-on:highlightParent="onHighlight(comment)" v-on:removeHighlightParent="onRemoveHighlight"></comment-list>
      </div>
    </div>
  </div>
</template>
<script>
import { mapState } from 'vuex'
import { postComment } from '@/api'
export default {
  name: 'commentList',
  props: {
    level: {
      type: Number,
      default: 0
    },
    comments: {
      type: Array,
      default: []
    },
    parent: {
      type: Object,
      default: null
    }
  },
  computed: {
    ...mapState({
      user: state => state.app.user
    })
  },
  data() {
    return {
      message: '',
      replyFieldShowIds: [],
      highlightCommentId: null,
    }
  },
  methods: {
    showReplyField(id) {
      if (!this.user) {
        this.$store.commit('app/setSignInDialogShow', true)
      } else {
        this.replyFieldShowIds.push(id)
      }
    },
    hideReplyField(id) {
      let index = this.replyFieldShowIds.indexOf(id)
      this.replyFieldShowIds.splice(index, 1)
    },
    postComment(index, parent_comment_id) {
      postComment({
        content: this.message,
        parent_comment_id
      }).then(res => {
        this.message = ''
        this.hideReplyField(index)
        this.$store.dispatch('app/getComments')
      }).catch(res => {
      })
    },
    onHighlight(comment) {
      this.highlightCommentId = comment.comment.id
    },
    onRemoveHighlight() {
      this.highlightCommentId = null
    },
    removeHighlightParent() {
      this.$emit('removeHighlightParent')
    },
    highlightParent() {
      this.$emit('highlightParent')
    }
  }
}
</script>