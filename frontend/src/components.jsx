function Footer(props: any) {
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

export {Footer, user_is_logged_in, get_user}