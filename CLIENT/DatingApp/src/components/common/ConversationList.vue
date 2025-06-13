<template>
  <div class="conversation-list">
    <div 
      v-for="conv in conversations" 
      :key="conv.conversation_id"
      class="conversation-item"
      :class="{ active: isActive(conv) }"
      @click="selectConversation(conv.conversation_id)"
    >
      <img 
        :src="getAvatar(conv.other_user)" 
        class="avatar"
        alt="User avatar"
      >
      <div class="info">
        <h4>{{ getUsername(conv.other_user) }}</h4>
        <p class="preview">{{ truncate(conv.last_message?.content, 50) }}</p>
      </div>
      <div class="meta">
        <span class="time">{{ formatTime(conv.last_message?.sent_at) }}</span>
        <span 
          v-if="conv.unread_count > 0" 
          class="badge"
        >
          {{ conv.unread_count }}
        </span>
      </div>
    </div>
  </div>
</template>

<script >
export default {
  props: {
    conversations: {
      type: Array,
      required: true,
      default: () => [],
      validator: (value) => {
        return Array.isArray(value) && 
          value.every(item => typeof item?.conversation_id !== 'undefined')
      }
    },
    currentConversation: {
      type: Object,
      default: null
    }
  },
  methods: {
    isActive(conv) {
      return this.currentConversation?.id === conv.conversation_id
    },
    selectConversation(id) {
      this.$emit('select', id)
    },
    getAvatar(user) {
      return user?.avatar || '/default-avatar.png'
    },
    getUsername(user) {
      return user?.name || 'Unknown User'
    },
    truncate(text, length = 50) {
      if (!text) return ''
      return text.length > length 
        ? text.substring(0, length) + '...' 
        : text
    },
    formatTime(dateString) {
      if (!dateString) return ''
      try {
        const date = new Date(dateString)
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      } catch {
        return ''
      }
    }
  }
}
</script>

<style scoped>
/* Your existing styles are good, no changes needed */
.conversation-list {
  overflow-y: auto;
}

.conversation-item {
  display: flex;
  padding: 12px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  align-items: center;
}

.conversation-item:hover {
  background-color: #f5f5f5;
}

.conversation-item.active {
  background-color: #e9f5ff;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 12px;
  object-fit: cover;
}

.info {
  flex: 1;
  min-width: 0;
}

.info h4 {
  margin: 0 0 4px;
  font-size: 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.info .preview {
  margin: 0;
  color: #666;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-left: 12px;
}

.time {
  font-size: 12px;
  color: #999;
}

.badge {
  background-color: #4a6cf7;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  margin-top: 4px;
}
</style>