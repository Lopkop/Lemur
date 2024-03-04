function Footer() {
	return <footer>Created by <a href="https://github.com/Lopkop">Lopkop</a></footer>
}

async function get_user() {
    const token = localStorage.getItem('token')
    if (!token) {
        return false;
    }
    const user = await fetch("http://localhost:8000/get_user/" + `${token}`, {
        method: 'GET',
        }).then(response => response.json());
    if (user.status == 400) {
        return false;
    }
    return user
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
        }
    }).then(response => response.json());

    if (response.status === 201) {
        localStorage.chat = response.chatroom.name
        window.location.pathname = `/chat/${response.chatroom.name}`;
    }
}


export {Footer, user_is_logged_in, get_user, createChat}