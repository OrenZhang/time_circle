<template>
    <div class="category-item" :style="{ 'backgroundColor': bg }">
        {{ data.name }}
    </div>
</template>

<script setup>
    import { computed, ref } from 'vue'

    const props = defineProps({
        data: {
            type: Object,
            default: {}
        },
        index: {
            type: Number,
            default: 0
        }
    })
    
    const bg = computed(() => {
        if (props.index % 3 === 1) {
            return 'var(--td-success-color-4)'
        }
        if (props.index % 3 === 2) {
            return 'var(--td-error-color-5)'
        }
        return 'var(--td-brand-color-5)'
    })
</script>

<style scoped>
.category-item {
    width: 100%;
    height: 140px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    margin-bottom: 20px;
    box-shadow: var(--td-shadow-1);
}

.category-item:hover {
    box-shadow: var(--td-shadow-3);
    cursor: pointer;
}

@media screen and (max-width: 1600px) {
    .category-item {
        height: 120px;
    }
}

@media screen and (max-width: 1200px) {
    .category-item {
        height: 120px;
    }
}
</style>