import { defineStore } from 'pinia'
import api from '@/composables/apiConnection'

export const useMessagesStore = defineStore('messages', {
  state: () => ({
    conversations: [],
    currentMessages: [],
    currentConversation: null
  }),
  
  actions: {
    async fetchConversations() {
      try {
        console.log('Fetching conversations...') // Debug log
        const response = await api.get('/messages/conversations')
        this.conversations = response.data?.conversations || []
        console.log('Fetched conversations:', this.conversations) // Debug log
        return this.conversations
      } catch (error) {
        console.error("Failed to fetch conversations:", error)
        throw error
      }
    },
    
    async fetchMessages(conversationId) {
      if (!conversationId) {
        console.warn("No conversation ID provided")
        return
      }
      
      try {
        console.log(`Fetching messages for conversation ${conversationId}...`) // Debug log
        const response = await api.get(`/messages/${conversationId}`)
        this.currentMessages = response.data?.messages || []
        console.log('Fetched messages:', this.currentMessages) // Debug log
        return this.currentMessages
      } catch (error) {
        console.error("Failed to fetch messages:", error)
        throw error
      }
    },
    
    async sendMessage(content) {
      if (!content?.trim()) {
        throw new Error("Message cannot be empty")
      }
      
      if (!this.currentConversation?.conversation_id) {
        throw new Error("No conversation selected")
      }

      try {
        console.log('Sending message:', { // Debug log
          conversation_id: this.currentConversation.conversation_id,
          recipient_id: this.currentConversation.other_user?.id,
          content: content.trim()
        })
        
        const response = await api.post('/messages/send', {
          conversation_id: this.currentConversation.conversation_id,
          recipient_id: this.currentConversation.other_user?.id,
          content: content.trim()
        })

        console.log('Message sent successfully:', response.data) // Debug log
        await this.fetchMessages(this.currentConversation.conversation_id)
        return response.data
      } catch (error) {
        console.error("Send message failed:", {
          error: error.response?.data || error.message,
          config: error.config
        })
        throw error
      }
    }
  }
})