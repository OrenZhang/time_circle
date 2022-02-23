<template>
    <div
        class="circle-item" :style="{ 'backgroundColor': bg, 'color': color }">
        {{ title }}
    </div>
</template>

<script setup>
    defineProps({
        title: {
            type: String,
            default: ''
        },
        color: {
            type: String,
            default: 'var(--td-font-white-1)'
        },
        bg: {
            type: String,
            default: 'var(--td-brand-color-5)'
        }
    })
</script>

<style scoped>
.circle-item {
    width: 180px;
    height: 180px;
    padding: 20px;
    box-sizing: border-box;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: var(--td-shadow-1);
}

.circle-item:hover {
    box-shadow: var(--td-shadow-3);
    cursor: pointer;
}

@media screen and (max-width: 1200px) {
    .circle-item {
        width: 140px;
        height: 140px;
        font-size: 20px;
    }
}

@media screen and (max-width: 800px) {
    .circle-item {
        width: 100px;
        height: 100px;
        font-size: 18px;
    }
}
</style>