function Footer() {
	return <footer>Created by <a href="https://github.com/Lopkop">Lopkop</a></footer>
}

async function get_user() {
    try {
        const response = await fetch("http://localhost:8000/get_user", {
            method: 'GET',
            credentials: 'include'
        });
        const user = await response.json();

        if (response.status == 401 || response.status === 400 || user.message === "Incorrect username or password" || user.message === "Token was not provided") {
            return false;
        }
        return user;
    } catch (error) {
        console.error("Error fetching user:", error);
        return false;
    }
}

async function user_is_logged_in() {
    let user = await get_user();
    if (user) {
        return true;
    } else {
        return false;
    }
}

async function createChat(event) {
    let user = await get_user()

    let response = await fetch("http://localhost:8000/create-chat?username=" + `${user.name}`, {
        method: 'POST',
        headers: {
        "Content-type": "application/json"
        },
        credentials: 'include'
    }).then(response => response.json());

    if (response.status === 201) {
        localStorage.chat = response.chatroom.name
        window.location.pathname = `/chat/${response.chatroom.name}`;
    }
}

// setInterval(showTime, 1000);
function showTime() {
    let time = new Date();
    let hour = time.getHours();
    let min = time.getMinutes();
    let sec = time.getSeconds();
}

export {Footer, user_is_logged_in, get_user, createChat}