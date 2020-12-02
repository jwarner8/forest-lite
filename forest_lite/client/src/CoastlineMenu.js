import React from "react"
import { useSelector, useDispatch } from "react-redux"
import { setFlag } from "./actions.js"
import "./CoastlineMenu.css"


const CoastlineMenu = () => {
    return (<>
        <div className="label">Coastlines, borders and lakes</div>
        <CoastlinesToggle />
    </>)
}


const CoastlinesToggle = () => {
    const selector = ({ coastlines: active = true }) => active
    const active = useSelector(selector)
    const dispatch = useDispatch()
    const onChange = ev => {
        const action = setFlag({
            coastlines: ev.target.checked
        })
        dispatch(action)
    }
    return (
        <div>
            <fieldset>
            <label>
                <input
                    type="checkbox"
                    checked={ active }
                    onChange={ onChange } />
                Coastlines
            </label>
            </fieldset>
        </div>
    )

}


export default CoastlineMenu
