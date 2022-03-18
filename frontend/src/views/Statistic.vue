<template>
    <div id="st-container">
        <t-loading :loading="loading" text="数据生成中..." :show-overlay="false" fullscreen />
        <div v-show="curCard === 'year'" class="w100-h100-flex date-picker">
            <t-select
                v-model="curYear"
                :bordered="true"
                style="width: 200px"
                :options="options"
            />
            <t-button variant="outline" @click="startTracking" :disabled="!curYear">
                发起回溯
            </t-button>
        </div>
        <div v-show="curCard === 'empty'" class="w100-h100-flex empty-card" />
        <div
            v-show="curCard === 'statistic' && dataIndex === index" class="w100-h100-flex statistic-box"
            v-for="(value, card, index) in data" :key="index">
            <transition>
                <component
                    :is="getComponent(card)"
                    :data="value" :has-next="hasNext" :has-last="hasLast"
                    @last="last" @next="next"
                />
            </transition>
        </div>
    </div>
</template>

<script setup>
    import { computed, onMounted, ref } from 'vue'
    import StHome from '../components/StHome.vue'
    import StEncounter from '../components/StEncounter.vue'
    import StMorning from '../components/StMorning.vue'
    import StEvening from '../components/StEvening.vue'
    import StRank from '../components/StRank.vue'
    import { getStatisticDataAPI, yearOptionsAPI } from '../api/statistic'
    import { MessagePlugin } from 'tdesign-vue-next'

    const getComponent = (card) => {
        if (card === 'home') {
            return StHome
        }
        if (card === 'encounter') {
            return StEncounter
        }
        if (card === 'morning') {
            return StMorning
        }
        if (card === 'evening') {
            return StEvening
        }
        if (card === 'rank') {
            return StRank
        }
    }

    const loading = ref(false)
    const setLoading = (status) => {
        if (status) {
            loading.value = true
        } else {
            setTimeout(() => {
                loading.value = false
            }, 2000)
        }
    }

    const curCard = ref('year')
    const dataIndex = ref(0)

    const data = ref({})

    const hasNext = computed(() => dataIndex.value < Object.keys(data.value).length - 1)
    const hasLast = computed(() => dataIndex.value > 0)
    const next = () => {
        if (hasNext.value) {
            dataIndex.value++
        }
    }
    const last = () => {
        if (hasLast.value) {
            dataIndex.value--
        }
    }
    
    const curYear = ref('')
    const options = ref([])
    const loadOptions = () => {
        yearOptionsAPI().then(
            res => options.value = res.data.data,
            err => MessagePlugin.error(err.data.msg)
        )
    }
    onMounted(loadOptions)

    const startTracking = () => {
        curCard.value = 'empty'
        setLoading(true)
        getStatisticDataAPI(curYear.value).then(
            res => data.value = res.data.data,
            err => MessagePlugin.error(err.data.msg)
        ).finally(() => {
            curCard.value = 'statistic'
            setLoading(false)
        })
    }
</script>

<style scoped>
#st-container {
    width: 100%;
    height: 100%;
    font-family: TencentSansW3, sans-serif;
}

.w100-h100-flex {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.date-picker {
    background: linear-gradient(30deg, #a8edea 0%, #fed6e3 100%);
}

.date-picker :deep(.t-select) {
    background: unset;
    border: 1px solid white;
}

.date-picker :deep(.t-select) .t-select__single,
.date-picker :deep(.t-select) .t-select__placeholder {
    color: white;
}

.date-picker :deep(.t-select) .t-select__right-icon {
    color: white;
}

.date-picker .t-button {
    background: none;
    border: 1px solid white;
    margin-left: 20px;
}

.date-picker .t-button :deep(.t-button__text) {
    color: white;
}

.empty-card {
    background: linear-gradient(30deg, #a8edea 0%, #fed6e3 100%);
}

.t-loading {
    background: linear-gradient(30deg, #a8edea 0%, #fed6e3 100%);
}

.t-loading :deep(.t-loading__text) {
    color: white;
}

.t-loading :deep(.t-icon-loading) .t-loading__gradient-conic {
    background: conic-gradient(from 90deg at 50% 50%, rgba(0, 82, 217, 0) 0deg, rgb(255, 255, 255) 360deg) !important;
}
</style>