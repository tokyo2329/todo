<script setup>
const runtimeConfig = useRuntimeConfig();
const toast = useToast();

const new_task_modal_open = ref(false);
const edit_task_modal_open = ref(false);
const edit_task_reference = ref(null);

const { data: tasks } = await useFetch(runtimeConfig.public.apiUrl + "/tasks", {
  watch: [new_task_modal_open, edit_task_modal_open],
});

const handle_check_completed = async (task) => {
  task.is_done = !task.is_done;

  await useFetch(runtimeConfig.public.apiUrl + "/tasks/" + task.id, {
    method: "PUT",
    body: task,
  });

  toast.add({ title: "Task has been updated!", color: "blue" });
};

const handle_delete = async (task) => {
  await useFetch(runtimeConfig.public.apiUrl + "/tasks/" + task.id, {
    method: "DELETE",
  });

  tasks.value = tasks.value.filter((t) => t.id != task.id);

  toast.add({ title: "Task has been deleted", color: "red" });
};

const columns = [
  {
    key: "name",
    label: "Name",
  },
  {
    key: "is_done",
    label: "Done",
  },
  {
    key: "actions",
  },
];

const options_dropdown = (task) => [
  [
    {
      label: "Mark as completed",
      click: () => handle_check_completed(task),
      disabled: task.is_done == true,
    },
  ],
  [
    {
      label: "Edit",
      click: () => {
        edit_task_reference.value = task;
        edit_task_modal_open.value = true;
      },
    },
    {
      label: "Delete",
      click: () => handle_delete(task),
    },
  ],
];
</script>

<template>
  <UContainer class="space-y-8">
    <h1 class="text-5xl font-semibold">Task list</h1>

    <UButton label="Add new" @click="new_task_modal_open = true" />

    <UTable :columns="columns" :rows="tasks">
      <template #is_done-data="{ row }">
        <UCheckbox
          v-model="row.is_done"
          class="flex"
          @click="handle_check_completed(row)"
        />
      </template>

      <template #actions-data="{ row }">
        <UDropdown :items="options_dropdown(row)">
          <UButton
            icon="i-heroicons-ellipsis-horizontal"
            color="gray"
            variant="ghost"
          />
        </UDropdown>
      </template>
    </UTable>

    <TaskCreateModal v-model="new_task_modal_open" />
    <TaskEditModal
      v-if="edit_task_modal_open"
      v-model="edit_task_modal_open"
      :task="edit_task_reference"
    />
  </UContainer>
</template>
