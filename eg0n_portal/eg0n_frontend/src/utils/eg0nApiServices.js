import axios from "axios";

class eg0nApiService {
  static GetVulns(filter) {
    const csrftoken = this.getCookie("csrftoken");
    return axios.post("./Vulns", filter, {
      headers: {
        "X-CSRFToken": csrftoken,
      },
    });
  }

  static getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
}

export { eg0nApiService };
