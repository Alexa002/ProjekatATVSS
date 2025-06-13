<template>
  <div class="message-input-container">
    <input
      v-model="message"
      @keyup.enter="sendMessage"
      placeholder="Type your message..."
      ref="inputField"
    />
    <button @click="sendMessage">Send</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['send'])
const message = ref('')
const inputField = ref(null)

const sendMessage = () => {
  if (message.value.trim()) {
    emit('send', message.value)
    message.value = ''
    inputField.value?.focus() // Keep focus on input after sending
  }
}
</script>

<style scoped>
.message-input-container {
  display: flex;
  padding: 10px;
  background: white;
  border-top: 1px solid #eee;
  position: sticky;
  bottom: 0;
}

input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  margin-right: 10px;
  outline: none;
}

button {
  padding: 10px 20px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

button:hover {
  background: #45a049;
}
</style>