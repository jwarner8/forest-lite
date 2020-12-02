import React from "react"
import { Provider } from "react-redux"
import { render, screen, fireEvent } from "@testing-library/react"
import "@testing-library/jest-dom/extend-expect"
import CoastlineMenu from "../src/CoastlineMenu.js"
import { createStore } from "../src/create-store.js"


test("CoastlineMenu", () => {
    const store = createStore()
    render(
        <Provider store={ store } >
            <CoastlineMenu />
        </Provider>
    )
    expect(screen.getByText(/coastlines, borders and lakes/i)).toBeInTheDocument()
})
