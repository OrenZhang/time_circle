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
                    {{ countInfo.id !== 0 ? '停止计时' : '开始计时' }}
                </t-button>
            </div>
        </div>
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
    const refreshInterval = ref(null)
    onMounted(() => {
        refreshInterval.value = setInterval(() => {
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
    })
    onBeforeUnmount(() => {
        clearInterval(refreshInterval.value)
    })

    const countInfo = ref({
        'id': 0,
        'category_id': 0,
        'start_at': ''
    })
    const countControl = () => {
        setLoading(true)
        if (countInfo.value.id === 0) {
            startItemAPI({ 'category_id': currentCategory.value }).then(
                res => countInfo.value = res.data.data,
                err => MessagePlugin.error(err.data.msg)
            ).finally(() => setLoading(false))
        } else {
            const endAt = moment().format('YYYY-MM-DD HH:mm:ss')
            stopItemAPI(countInfo.value.id, { end_at: endAt }).then(
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

.buttons .t-button {
    height: 100%;
    border: 2px solid var(--td-gray-color-3);
}

.buttons :deep(.t-button--variant-text) {
    padding-left: 20px;
    padding-right: 20px;
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