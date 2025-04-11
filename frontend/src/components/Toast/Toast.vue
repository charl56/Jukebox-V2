<template>
    <div class="toast-container" v-if="visible">
        <div class="toast">
            <div class="toast-header">
                <h3>{{ title }}</h3>
                <button class="close-button" @click="close">×</button>
            </div>
            <div class="toast-body">
                {{ content }}
            </div>
        </div>
    </div>
</template>

<script>
import { eventBus } from '@/plugins/eventBus.js'

export default {
    name: 'Toast',
    data() {
        return {
            visible: false,
            duration: 5000,
            autoClose: true,
            timer: null
        }
    },
    created() {
        eventBus.on('showToast', (data) => {
            this.title = data.title
            this.content = data.content
            this.show()
        })
    },
    methods: {
        show() {
            this.visible = true

            if (this.autoClose) {
                clearTimeout(this.timer)
                this.timer = setTimeout(() => {
                    this.close()
                }, this.duration)
            }
        },
        close() {
            this.visible = false
            clearTimeout(this.timer)
            this.$emit('close')
        }
    },
    beforeDestroy() {
        clearTimeout(this.timer)
    }
}
</script>

<style scoped>
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
}

.toast {
    min-width: 250px;
    max-width: 350px;
    background-color: #565656;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    overflow: hidden;
}

.toast-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    background-color: #656565;
}

.toast-header h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 500;
}

.close-button {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    padding: 0;
    margin-left: 10px;
    color: #888;
}

.toast-body {
    padding: 15px;
    word-wrap: break-word;
}
</style>
