export function Footer(props: any) {
	return <footer>Created by <a href="https://github.com/Lopkop">Lopkop</a></footer>
}

export function getUser() {
    // fetch user from access token
    localStorage.getItem("user");
}