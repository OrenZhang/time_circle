<template>
    <div class="st-home-box">
        <div style="font-size: 16px">
            {{ data.item_date }} {{ data.start_at }}
        </div>
        <div style="font-size: 18px">
            为了 <span class="total_count">{{ data.item_name }}</span> 匆匆早起
        </div>
        <div>
            <div style="font-size: 16px">
                忙碌了 <span class="total_minute">{{ transTime2Minutes(data.item_duration) }}</span> 分钟
            </div>
        </div>
        <img src="/extra-assets/imgs/st-morning-bg.png" alt="st-home-bg.png" class="bg-img">
        <div class="arrow-box">
            <i class="fa-solid fa-angle-up" v-show="hasLast" @click="$emit('last')" />
            <i class="fa-solid fa-angle-down" v-show="hasNext" @click="$emit('next')" />
        </div>
    </div>
</template>

<script setup>
    import moment from 'moment'

    defineProps({
        data: {
            type: Object,
            default: {
                item_name: 'Work',
                item_duration: 3600,
                item_date: '1月10日',
                start_at: '06:21'
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