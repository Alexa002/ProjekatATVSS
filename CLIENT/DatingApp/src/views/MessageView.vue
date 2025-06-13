<script setup>
import { onMounted } from 'vue'
import { useMessagesStore } from '@/stores/message'
import { useAuthStore } from '@/stores/auth'
import MessageInput from '@/components/common/MessageInput.vue'
import MessageList from '@/components/common/MessageList.vue'

const messagesStore = useMessagesStore()
const authStore = useAuthStore()

// Load conversations on mount
onMounted(async () => {
  try {
    await messagesStore.fetchConversations()
  } catch (error) {
    console.error("Failed to load conversations:", error)
  }
})

// Handle conversation selection
const selectConversation = async (conversation) => {
  try {
    messagesStore.currentConversation = conversation
    await messagesStore.fetchMessages(conversation.conversation_id)
  } catch (error) {
    console.error("Failed to load messages:", error)
  }
}

// Send message handler
const sendMessage = async (content) => {
  try {
    await messagesStore.sendMessage(content)
  } catch (error) {
    console.error("Failed to send message:", error)
  }
}
</script>

<template>
  <div class="messaging-container">
    <!-- Conversation list -->
    <div class="conversation-list">
      <h2>Conversations</h2>
      <div 
        v-for="conversation in messagesStore.conversations" 
        :key="conversation.conversation_id"
        @click="selectConversation(conversation)"
        :class="{ active: messagesStore.currentConversation?.conversation_id === conversation.conversation_id }"
        class="conversation-item"
      >
        <div class="conversation-info">
          <strong>{{ conversation.other_user?.name || 'Unknown' }}</strong>
          <p class="last-message">
            {{ conversation.last_message?.content || 'No messages yet' }}
          </p>
        </div>
      </div>
    </div>

    <!-- Message area -->
    <div class="message-area">
      <div v-if="messagesStore.currentConversation" class="message-content">
        <div class="message-header">
          <h3>{{ messagesStore.currentConversation.other_user?.name || 'Chat' }}</h3>
        </div>
        
        <MessageList 
          :messages="messagesStore.currentMessages" 
          :currentUserId="authStore.user?.id" 
        />
        
        <MessageInput @send="sendMessage" />
      </div>
      
      <div v-else class="empty-state">
        <p>Select a conversation</p>
      </div>
    </div>
  </div>
</template>


<style scoped>
.messaging-container {
  display: flex;
  height: 100vh;
}

.conversation-list {
  width: 300px;
  border-right: 1px solid #eee;
  padding: 10px;
  overflow-y: auto;
}

.conversation-item {
  padding: 12px;
  margin-bottom: 8px;
  cursor: pointer;
  border-radius: 8px;
}

.conversation-item:hover {
  background: #f5f5f5;
}

.conversation-item.active {
  background: #e6f7ff;
}

.last-message {
  color: #666;
  font-size: 0.8rem;
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.message-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.message-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
}
</style>