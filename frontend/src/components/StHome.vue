<template>
    <div class="st-home-box">
        <div style="font-size: 18px">
            共使用 Time Circle 记录 <span class="total_count">{{ data.total_count }}</span> 次
        </div>
        <div>
            <div style="font-size: 16px">
                累计处理 <span class="total_hour">{{ transTime(data.total_time) }}</span> 小时事项，约 <span class="total_minute">{{ transTime2Minutes(data.total_time) }}</span> 分钟
            </div>
        </div>
        <img src="/extra-assets/imgs/st-home-bg.png" alt="st-home-bg.png" class="bg-img">
        <div class="arrow-box">
            <i class="fa-solid fa-angle-up" v-if="hasLast" @click="$emit('last')" />
            <i class="fa-solid fa-angle-down" v-if="hasNext" @click="$emit('next')" />
        </div>
    </div>
</template>

<script setup>
    import moment from 'moment'

    defineProps({
        data: {
            type: Object,
            default: {
                'total_time': 0,
                'total_count': 0
            }
        },
        hasNext: {
            type: Boolean,
            default: false
        },
        hasLast: {
            type: Boolean,
            default: false
        }
    })
    defineEmits(['last', 'next'])

    const transTime = (seconds) => parseInt(moment.duration(seconds, 'seconds').asHours())
    const transTime2Minutes = (seconds) => parseInt(moment.duration(seconds, 'seconds').asMinutes())
</script>

<style scoped>
.st-home-box {
    min-width: 360px;
    width: 100%;
    height: 100%;
    color: white;
    background-image: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 100%);
    box-sizing: border-box;
    padding: 20px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.total_count {
    color: var(--td-brand-color-5);
    font-size: 32px;
    line-height: 60px;
}

.total_hour {
    color: var(--td-brand-color-5);
    font-size: 24px;
    line-height: 40px;
}

.total_minute {
    color: var(--td-brand-color-5);
    font-size: 24px;
    line-height: 40px;
}

.bg-img {
    width: 100%;
    max-width: 360px;
}

.arrow-box {
    display: flex;
}

.arrow-box i {
    font-size: 24px;
}

.arrow-box i:nth-of-type(2) {
    margin-left: 36px;
}
</style>