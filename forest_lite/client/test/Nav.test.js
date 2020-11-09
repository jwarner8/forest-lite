import React from "react"
import { Provider } from "react-redux"
import { selectDatasets, selectActive } from "../src/Nav.js"
import { render, unmountComponentAtNode } from "react-dom"
import { act } from "react-dom/test-utils"
import { NavPanel } from "../src/Nav.js"
import { createStore } from "../src/create-store.js"


test("selectDatasets", () => {
    const actual = selectDatasets({})
    const expected = []
    expect(actual).toEqual(expected)
})


test("selectDatasets given realistic data", () => {
    const content = [
        {key: "value"}
    ]
    const actual = selectDatasets({ datasets: content })
    const expected = content
    expect(actual).toEqual(expected)
})


test("selectActive", () => {
    const dataset = {
        label: "Label",
        datasetId: 42,
        active: { foo: false, bar: true }
    }
    const actual = selectActive({ datasets: [
        dataset
    ] })
    const expected = [
        {
            label: "Label",
            id: 42,
            dataVar: "bar"
        }
    ]
    expect(actual).toEqual(expected)
})


beforeAll(() => {
})

let container = null
beforeEach(() => {
    container = document.createElement("div")
    document.body.appendChild(container)
})


afterEach(() => {
    unmountComponentAtNode(container)
    container.remove()
    container = null
})


test("NavPanel", async () => {
    const store = createStore()

    // Fake fetch API
    window.fetch = jest.fn().mockImplementation(url => {
        return Promise.resolve({
            json: () => Promise.resolve({})
        })
    })

    // Asynchronous act() to resolve promises
    await act(async () => {
        render(
            <Provider store={store}>
                <NavPanel
                    baseURL=""
                    datasetName={ null }
                    dataVar={ null } />
            </Provider>, container)
    })

    expect(container.textContent).toEqual("")

    // Restore original fetch function
    window.fetch.mockClear()
    delete window.fetch
})
