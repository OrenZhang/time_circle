<template>
    <div class="login-container">
        <div class="login-box">
            <t-form
                :data="loginData" :colon="true" :label-width="0" :rules="rules" :success-border="true"
                @submit="onSubmit">
                <t-form-item name="username">
                    <t-input v-model="loginData.username" clearable placeholder="请输入用户名">
                        <template #prefix-icon>
                            <desktop-icon />
                        </template>
                    </t-input>
                </t-form-item>
                <t-form-item name="password">
                    <t-input v-model="loginData.password" type="password" clearable placeholder="请输入密码">
                        <template #prefix-icon>
                            <lock-on-icon />
                        </template>
                    </t-input>
                </t-form-item>
                <t-form-item style="padding-top: 8px">
                    <t-button theme="primary" type="submit" block>
                        登录
                    </t-button>
                </t-form-item>
            </t-form>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue'
    import { DesktopIcon, LockOnIcon } from 'tdesign-icons-vue-next'
    import { loginAPI } from '../api/user'
    import { MessagePlugin } from 'tdesign-vue-next'
    import { useStore } from 'vuex'
    import { useRouter } from 'vue-router'

    const store = useStore()
    const router = useRouter()

    const loginData = ref({
        username: '',
        password: ''
    })
    const rules = ref({
        username: [
            { required: true, message: '必填', type: 'error' },
        ],
        password: [
            { required: true, message: '必填', type: 'error' }
        ],
    })

    const onSubmit = (context) => {
        if (context.validateResult !== true) {
            return
        }
        loginAPI(loginData.value).then(
            res => {
                MessagePlugin.success('登录成功')
                store.dispatch('getUserInfo')
                router.push({ name: 'Home' })
            },
            err => MessagePlugin.error(err.data.msg)
        )
    }
</script>

<style scoped>
.login-container {
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-box {
    max-width: 240px;
    width: 100%;
}
</style>