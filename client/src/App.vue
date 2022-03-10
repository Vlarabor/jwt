<template>
  <div class="container">
    <h1>You are {{ loggedIn ? "" : "not" }} logged in!</h1>
    <div>
      <div v-if="loggedIn">
        <Token />
      </div>
      <div v-else>
        <form @submit.prevent="login">
          <label>
            Username
            <input v-model="username" type="text" />
          </label>
          <label>
            Password
            <input v-model="password" type="password" />
          </label>
          <button type="submit">Log In</button>
        </form>
      </div>
    </div>
    <p>Access Token:</p>
    <div class="token">{{ accessToken }}</div>
    <p>Refresh Token:</p>
    <div class="token">{{ refreshToken }}</div>
  </div>
</template>

<script>
import Token from "@/components/Token.vue";
import axios from "axios";
import { ref } from "vue";
import { useStore, mapState } from "vuex";

export default {
  name: "App",
  components: {
    Token,
  },
  setup() {
    const store = useStore();
    const username = ref("");
    const password = ref("");

    const login = async () => {
      try {
        const response = await axios.post(
          "http://localhost:5000/token",
          undefined,
          {
            withCredentials: true,
            auth: {
              username: username.value,
              password: password.value,
            },
          }
        );
        username.value = "";
        password.value = "";
        store.dispatch("loginUser", {
          accessToken: response.data.accessToken,
          refreshToken: response.data.refreshToken,
        });
      } catch (err) {
        password.value = "";
        alert(`Error: ${err?.response?.data?.errors}`);
      }
    };

    return { username, password, login };
  },
  computed: {
    ...mapState(["loggedIn", "accessToken", "refreshToken"]),
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1.25rem;
}

input {
  margin-left: 0.25rem;
}

p {
  font-size: 2rem;
  text-align: center;
}

.container {
  max-width: 1300px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.token {
  max-width: 50ch;
  width: 50ch;
  overflow-wrap: break-word;
}
</style>
