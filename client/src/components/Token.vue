<template>
  <div>
    <a @click.prevent="onClick"> SEND REQUEST </a>
  </div>
</template>

<script>
import axios from "axios";
import { useStore, mapState } from "vuex";

export default {
  name: "Token",
  setup() {
    const store = useStore();

    const onClick = async () => {
      try {
        const response = await axios.get("http://localhost:5000/token", {
          headers: {
            accessToken: store.state.accessToken,
            refreshToken: store.state.refreshToken,
          },
          withCredentials: true,
        });
        if (response.data.errors) {
          alert(`Error: ${response.data.errors}`);
        } else {
          alert(`Success: ${response.data.msg}`);
        }
      } catch (err) {
        alert(`Error: ${err?.response?.data?.errors}`);
        store.dispatch("logoutUser");
      }
    };

    return { onClick };
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

a {
  padding: 1rem;
  background: chocolate;
  color: white;
  margin: 1rem;
  cursor: pointer;
}
</style>
