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
                    :disabled="countInfo.id !== 0" placeholder="-请选择-" v-model="currentCategory" :options="categories"
                    filterable :keys="{ value: 'id', label: 'full_name' }" :bordered="false" />
                <t-button theme="default" variant="text" :disabled="!currentCategory" @click="countControl">
                    {{ countInfo.id !== 0 ? '停止计时' : '开始计时' }}
                </t-button>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { onMounted, onUnmounted, ref } from 'vue'
    import { useRouter } from 'vue-router'
    import { loadCategoriesAPI, startItemAPI, stopItemAPI } from '../api/circle'
    import { MessagePlugin } from 'tdesign-vue-next'
    import moment from 'moment'

    const router = useRouter()

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
        const now = new Date()
        const dateDiff = now.getTime() - countInfo.value.start_at.getTime()
        let leftDiff, hour, minute, second
        hour = Math.floor(dateDiff / (3600 * 1000))
        leftDiff = dateDiff % (3600 * 1000)
        minute = Math.floor(leftDiff / (60 * 1000))
        leftDiff = leftDiff % (60 * 1000)
        second = Math.round(leftDiff / 1000)
        timeCount.value = formatNumber(hour) + ':' + formatNumber(minute) + ':' + formatNumber(second)
    }, 1000)
    onUnmounted(() => {
        clearInterval(refreshInterval.value)
    })

    const countInfo = ref({
        'id': 0,
        'category_id': 0,
        'start_at': new Date()
    })
    const countControl = () => {
        if (countInfo.value.id === 0) {
            startItemAPI({ 'category_id': currentCategory.value }).then(
                res => {
                    const data = res.data.data
                    data.start_at = new Date(data.start_at)
                    countInfo.value = data
                },
                err => MessagePlugin.error(err.data.msg)
            )
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
                },
                err => MessagePlugin.error(err.data.msg)
            )
        }
    }
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
    border: 2px solid var(--td-gray-color-6);
    border-radius: 5px;
}

.buttons {
    margin-top: 20px;
    display: flex;
}

.buttons :deep(.t-select__wrap) {
    border: 2px solid var(--td-gray-color-6);
    border-radius: 5px;
}

.buttons .t-button {
    height: 100%;
    border: 2px solid var(--td-gray-color-6);
    margin-left: 20px;
}

.buttons :deep(.t-button--variant-text) {
    padding-left: 20px;
    padding-right: 20px;
}
</style>