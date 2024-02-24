import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import CreateChat from './routes/CreateChat'
import ConnectToChat from './routes/ConnectToChat'
import Login from './routes/Login'
import SignUp from './routes/SignUp'
import ErrorPage from "./error-page";
import Chat from "./routes/Chat"
import Root from './routes/Root'
import Root2 from './routes/Root2'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/signup",
    element: <SignUp />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/login",
    element: <Login />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/chats",
    element: <Root2 />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/create_chat",
    element: <CreateChat />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/connect_chat",
    element: <ConnectToChat />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/chat/:chatName",
    element: <Chat />,
  },
]);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
    <RouterProvider router={router} />
);
