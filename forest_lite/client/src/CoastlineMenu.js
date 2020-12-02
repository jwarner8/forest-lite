import React from "react"
import { useSelector, useDispatch } from "react-redux"
import { setFlag } from "./actions.js"
import "./CoastlineMenu.css"


class Label extends React.Component {
    render() {
        return <div className="label">{ this.props.children }</div>
    }
}


const CoastlineMenu = () => {
    return (<>
        <Label>Coastlines, borders and lakes</Label>
        <fieldset>
        <CoastlinesToggle />
        </fieldset>
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
    return (<Item key="coastlines"
                  checked={ active }
                  onChange={ onChange }>Coastlines</Item>)

}


const Item = (props) => {
    const { checked, onChange, children } = props
    return (
        <div>
            <label>
                <input
                    type="checkbox"
                    checked={ checked }
                    onChange={ onChange } />
                { children }
            </label>
        </div>
    )
}


export default CoastlineMenu
