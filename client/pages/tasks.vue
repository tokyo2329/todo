<script setup>
const runtimeConfig = useRuntimeConfig();
const toast = useToast();

const tasks = ref([]);
const new_task_modal_open = ref(false);
const edit_task_modal_open = ref(false);
const edit_task_reference = ref(null);

const { data, pending, refresh } = await useFetch(
  runtimeConfig.public.apiUrl + "/tasks",
  {
    server: false,
    watch: [new_task_modal_open, edit_task_modal_open],
    onRequestError({ error }) {
      toast.add({
        title: "Fetching tasks failed",
        color: "red",
      });
    },
    onResponse({ response }) {
      console.log("data fetched");
      tasks.value = response._data;
    },
  },
);

const handle_check_completed = async (task) => {
  await useFetch(runtimeConfig.public.apiUrl + "/tasks/" + task.id, {
    method: "PUT",
    body: {
      id: task.id,
      name: task.name,
      is_done: !task.is_done,
    },
    onRequestError() {
      toast.add({ title: "Error while updating task!", color: "red" });
    },
    onResponse() {
      toast.add({ title: "Task has been updated!", color: "blue" });
    },
  });

  refresh();
};

const handle_delete = async (task) => {
  await useFetch(runtimeConfig.public.apiUrl + "/tasks/" + task.id, {
    method: "DELETE",
    onRequestError() {
      toast.add({ title: "Error while deleting task!", color: "red" });
    },
    onResponse() {
      toast.add({ title: "Task has been deleted!", color: "primary" });
    },
  });

  refresh();
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

    <div class="flex gap-x-2 items-center">
      <UButton label="Add new" @click="new_task_modal_open = true" />
      <UButton
        label="Refresh"
        variant="outline"
        @click="refresh"
        :loading="pending"
      />
    </div>

    <UTable :columns="columns" :rows="tasks" :loading="pending">
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
