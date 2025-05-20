<template>
  <div class="p-4 flex flex-col w-full">
    <h2 class="text-xl font-bold text-gray-700 mb-4">Adaugă sesiune</h2>
    <form
      class="flex flex-col w-full items-center mb-2 justify-center"
      @submit.prevent="addSession"
    >
      <div class="flex flex-wrap gap-6 mb-6">
        <select class="py-2 px-1" v-model="form.day">
          <option v-for="d in days" :key="d">{{ d }}</option>
        </select>
        <select class="py-2 px-1" v-model="form.slotId">
          <option v-for="s in timeSlots" :key="s.id" :value="s.id">
            {{ s.start }} - {{ s.end }}
          </option>
        </select>
        <select class="py-2 px-1" v-model="form.group">
          <option v-for="g in groups" :key="g">{{ g }}</option>
        </select>
        <select class="py-2 px-1" v-model="form.professor">
          <option v-for="p in professors" :key="p">{{ p }}</option>
        </select>
        <select class="py-2 px-1" v-model="form.discipline">
          <option v-for="d in disciplines" :key="d">{{ d }}</option>
        </select>
        <select class="py-2 px-1" v-model="form.type">
          <option v-for="t in activityTypes" :key="t">{{ t }}</option>
        </select>
        <select class="py-2 px-1" v-model="form.room">
          <option v-for="r in rooms" :key="r.name">{{ r.name }}</option>
        </select>
      </div>
      <button
        class="flex w-[300px] justify-center items-center bg-blue-300 shadow-md text-white px-4 py-2 text-lg rounded"
        type="submit"
      >
        Adaugă
      </button>
    </form>

    <h2 class="text-xl font-bold text-gray-700 mb-4">Orar</h2>
    <div class="grid grid-cols-6 gap-px text-gray-800 border border-blue-300">
      <div class="bg-blue-100 font-bold text-gray-700 p-2">Ora</div>
      <div v-for="day in days" :key="day" class="bg-blue-100 text-gray-700 font-bold p-2">
        {{ day }}
      </div>

      <div v-for="slot in timeSlots" :key="slot.id" class="contents">
        <div class="bg-blue-100 p-2 text-sm">
          {{ slot.start }} - {{ slot.end }}
        </div>

        <div
          v-for="day in days"
          :key="day"
          class="border border-blue-300 p-2 min-h-[5rem] bg-white"
        >
          <div
            v-for="s in sessions.filter(
              (s) => s.day === day && s.slotId === slot.id
            )"
            :key="s.group + s.discipline + s.professor + s.room"
            class="text-sm mb-2 p-1 text-gray-700 rounded bg-blue-100 relative"
          >
            <button
              class="absolute top-1 right-1 text-gray-600 hover:text-red-800 text-xs"
              @click="removeSession(s)"
            >
              x
            </button>
            <strong>{{ s.discipline }}</strong> ({{ s.type }})<br />
            {{ s.group }}<br />
            {{ s.professor }}<br />
            <em>{{ s.room }}</em>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const timeSlots = [
  { id: 1, start: "08:00", end: "10:00" },
  { id: 2, start: "10:00", end: "12:00" },
  { id: 3, start: "12:00", end: "14:00" },
  { id: 4, start: "14:00", end: "16:00" },
  { id: 5, start: "16:00", end: "18:00" },
];

const groups = ["Semian A", "Semian B", "Semian C"];
const professors = ["Prof. Smith", "Dr. Johnson", "Ms. Brown"];
const disciplines = ["Mathematics", "Physics", "Computer Science"];
const rooms = [
  { name: "Room 101", type: "curs" },
  { name: "Lab 1", type: "laborator" },
  { name: "Seminar Room 3", type: "seminar" },
];
const activityTypes = ["curs", "seminar", "laborator"];

const sessions = ref<any[]>([]);

const form = reactive({
  day: "Monday",
  slotId: 1,
  group: groups[0],
  professor: professors[0],
  discipline: disciplines[0],
  room: rooms[0].name,
  type: "curs",
});

const addSession = () => {
  // Validare duplicat absolut (aceeași sesiune deja adăugată complet)
  const duplicate = sessions.value.find(s =>
    s.day === form.day &&
    s.slotId === form.slotId &&
    s.group === form.group &&
    s.professor === form.professor &&
    s.discipline === form.discipline &&
    s.type === form.type &&
    s.room === form.room
  )

  if (duplicate) {
    alert('Această sesiune este deja adăugată.')
    return
  }

  // Validare: aceeași grupă nu poate avea de două ori aceeași disciplină + același tip de activitate
  const alreadyScheduled = sessions.value.find(s =>
    s.group === form.group &&
    s.discipline === form.discipline &&
    s.type === form.type
  )

  if (alreadyScheduled) {
    alert(`Grupa ${form.group} are deja această activitate (${form.discipline} – ${form.type}) programată.`)
    return
  }

  // Validare existentă: conflict de profesor, grupă, sală în același slot
  const conflict = sessions.value.find(
    s =>
      s.day === form.day &&
      s.slotId === form.slotId &&
      (
        s.professor === form.professor ||
        s.group === form.group ||
        s.room === form.room
      )
  )

  if (conflict) {
    alert("Conflict detectat: profesorul, grupa sau sala este deja ocupată în acest interval.")
    return
  }

  sessions.value.push({ ...form })
}

const removeSession = (sessionToRemove: any) => {
  sessions.value = sessions.value.filter((s) => s !== sessionToRemove);
};
</script>
