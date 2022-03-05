<template>
    <div class="time-container">
        <t-breadcrumb>
            <t-breadcrumbItem v-for="item in breadItems" :key="item" @click="clickBread(item)">
                {{ item.title }}
            </t-breadcrumbItem>
        </t-breadcrumb>
        <div class="control-box">
            <div class="clock">
                {{ timeCount }}
            </div>
            <div class="buttons">
                <t-select
                    :disabled="countInfo.id !== 0" :loading="loading" placeholder="-请选择-" v-model="currentCategory" :options="categories"
                    filterable :keys="{ value: 'id', label: 'full_name' }" :bordered="false" />
                <t-button theme="default" variant="text" :loading="loading" :disabled="!currentCategory" @click="countControl">
                    {{ countInfo.id !== 0 ? '结束计时' : '开始计时' }}
                </t-button>
            </div>
        </div>
        <t-dialog
            v-model:visible="endAtVisible" :cancel-btn="null" :confirm-btn="null"
            header="确认时间" class="submit-dialog">
            <t-form label-width="60px" :colon="true" @submit="doEnd">
                <t-form-item label="开始" name="datetime">
                    <t-date-picker
                        theme="primary"
                        mode="date"
                        format="YYYY-MM-DD HH:mm:ss"
                        enable-time-picker
                        :disable-date="disableDate"
                        v-model:value="startAt"
                    />
                </t-form-item>
                <t-form-item label="结束" name="datetime">
                    <t-date-picker
                        theme="primary"
                        mode="date"
                        format="YYYY-MM-DD HH:mm:ss"
                        enable-time-picker
                        :disable-date="disableDate"
                        v-model:value="endAt"
                    />
                </t-form-item>
                <t-form-item style="padding-top: 8px" class="submit-button">
                    <t-button theme="primary" type="submit" style="margin-right: 10px">
                        提交
                    </t-button>
                </t-form-item>
            </t-form>
        </t-dialog>
    </div>
</template>

<script setup>
    import { onMounted, onBeforeUnmount, ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { loadCategoriesAPI, startItemAPI, stopItemAPI, todoItemAPI } from '../api/circle'
    import { MessagePlugin } from 'tdesign-vue-next'
    import moment from 'moment'

    const router = useRouter()

    const loading = ref(false)
    const setLoading = (status) => {
        if (status) {
            loading.value = true
        } else {
            setTimeout(() => {
                loading.value = false
            }, 600)
        }
    }

    const breadItems = ref([
        {
            path: { name: 'Home' },
            title: 'Home'
        },
        {
            path: 0,
            title: 'Time'
        }
    ])

    const clickBread = (item) => {
        if (typeof item.path === 'object') {
            router.push(item.path)
        }
    }

    const currentCategory = ref(null)
    const categories = ref([])
    const loadCategories = () => loadCategoriesAPI().then(
        res => categories.value = res.data.data,
        err => MessagePlugin.error(err.data.msg)
    )
    onMounted(loadCategories)

    const formatNumber = (num) => {
        if (String(num).length === 1) {
            return '0' + String(num)
        }
        return num
    }

    const timeCount = ref('00:00:00')
    const refreshInterval = setInterval(() => {
        if (countInfo.value.id === 0) {
            return
        }
        const now = new moment()
        const start = new moment(countInfo.value.start_at)
        const dateDiff = moment.duration(now.diff(start)).as('seconds')
        let leftDiff, hour, minute, second
        hour = Math.floor(dateDiff / 3600)
        leftDiff = dateDiff % 3600
        minute = Math.floor(leftDiff / 60)
        leftDiff = leftDiff % 60
        second = Math.round(leftDiff)
        timeCount.value = formatNumber(hour) + ':' + formatNumber(minute) + ':' + formatNumber(second)
    }, 1000)
    onBeforeUnmount(() => {
        clearInterval(refreshInterval)
    })

    const countInfo = ref({
        'id': 0,
        'category_id': 0,
        'start_at': ''
    })
    const startAt = ref(null)
    const endAt = ref(null)
    const endAtVisible = ref(false)
    const countControl = () => {
        if (countInfo.value.id === 0) {
            setLoading(true)
            startItemAPI({ 'category_id': currentCategory.value }).then(
                res => countInfo.value = res.data.data,
                err => MessagePlugin.error(err.data.msg)
            ).finally(() => setLoading(false))
        } else {
            startAt.value = countInfo.value.start_at
            endAt.value = new moment().format('YYYY-MM-DD HH:mm:ss')
            endAtVisible.value = true
        }
    }
    const doEnd = () => {
        endAtVisible.value = false
        setLoading(true)
        stopItemAPI(
            countInfo.value.id,
            { start_at: startAt.value, end_at: endAt.value }
        ).then(
            () => {
                countInfo.value = {
                    'id': 0,
                    'category_id': 0,
                    'start_at': null
                }
                timeCount.value = '00:00:00'
                currentCategory.value = null
                MessagePlugin.success('记录创建成功')
            },
            err => MessagePlugin.error(err.data.msg)
        ).finally(() => setLoading(false))
    }

    const loadTodoItem = () => todoItemAPI().then(
        res => {
            if (res.data.data.todo) {
                countInfo.value = res.data.data.item
                currentCategory.value = countInfo.value.category_id
            }
        }, err => MessagePlugin.error(err.data.msg)
    )
    onMounted(loadTodoItem)

    const disableDate = (date) => date > new Date()
</script>

<style scoped>
.time-container {
    height: 100%;
    width: 100%;
    padding: 20px;
    box-sizing: border-box;
}

.t-breadcrumb {
    padding-bottom: 20px;
}

.control-box {
    height: calc(100% - 50px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.clock {
    width: 480px;
    height: 240px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    font-size: 48px;
    border: 2px solid var(--td-gray-color-3);
    border-radius: 5px;
    color: var(--td-text-color-primary);
}

.buttons {
    margin-top: 20px;
    display: flex;
}

.buttons :deep(.t-select) {
    width: 100%;
    border: 2px solid var(--td-gray-color-3);
}

.buttons :deep(.t-select__wrap) {
    padding-right: 20px;
    width: 380px;
}

.t-date-picker {
    width: 100%;
}

.buttons .t-button {
    height: 100%;
    border: 2px solid var(--td-gray-color-3);
}

.buttons :deep(.t-button--variant-text) {
    padding-left: 20px;
    padding-right: 20px;
}

.submit-button :deep(.t-form__controls-content) {
    float: right;
}

.submit-button :deep(.t-form__controls-content) .t-button {
    margin-right: 0!important;
}

.submit-dialog :deep(.t-dialog__body) {
    padding-bottom: 0 !important;
}

@media screen and (max-width: 500px) {
    .clock {
        width: 100%;
    }
    .buttons {
        width: 100%;
    }
    .buttons :deep(.t-select__wrap) {
        overflow: hidden;
        width: 100%;
    }
}
</style>