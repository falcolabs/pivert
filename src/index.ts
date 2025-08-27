/**
 * Team Pivert's entry in VinFuture 2025. A simple and effective reminder app.
 * Copyright (C) 2025  Team Pivert
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import { mount } from "svelte";
import App from "./App.svelte";
import "./styles/preflight.css";
import "./styles/styles.sass";

const app = mount(App, {
    target: document.body,
});

export default app;
