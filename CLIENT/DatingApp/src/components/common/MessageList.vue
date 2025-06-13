<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'

const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  currentUserId: {
    type: Number,
    default: null
  }
})

const messagesContainer = ref(null)

// Format time function - now properly defined
const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Auto-scroll to bottom
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

watch(() => props.messages, () => {
  scrollToBottom()
}, { deep: true })

onMounted(() => {
  scrollToBottom()
})
</script>

<template>
  <div class="message-list-container" ref="messagesContainer">
    <div 
      v-for="message in messages" 
      :key="message.id"
      :class="['message', message.sender_id === currentUserId ? 'sent' : 'received']"
    >
      <div class="content">{{ message.content }}</div>
      <div class="time">{{ formatTime(message.sent_at) }}</div>
    </div>
  </div>
</template>

<style scoped>
.message-list-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.message {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 12px;
}

.sent {
  background: #dcf8c6;
  align-self: flex-end;
  border-bottom-right-radius: 0;
}

.received {
  background: #f1f1f1;
  align-self: flex-start;
  border-bottom-left-radius: 0;
}

.content {
  word-break: break-word;
}

.time {
  font-size: 0.7rem;
  color: #666;
  text-align: right;
  margin-top: 2px;
}
</style>