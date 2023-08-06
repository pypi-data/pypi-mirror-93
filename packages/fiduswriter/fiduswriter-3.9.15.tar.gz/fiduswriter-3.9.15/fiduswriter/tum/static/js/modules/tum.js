import {ensureCSS} from "./common"
export class TUMApp {
    constructor(app) {
        this.app = app
    }

    init() {
        return ensureCSS([
            'tum.css'
        ])
    }
}
