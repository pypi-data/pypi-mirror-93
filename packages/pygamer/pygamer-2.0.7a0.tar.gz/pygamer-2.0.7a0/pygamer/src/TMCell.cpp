// This file is part of the GAMer software.
// Copyright (C) 2016-2021
// by Christopher T. Lee and contributors
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, see <http://www.gnu.org/licenses/>
// or write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330,
// Boston, MA 02111-1307 USA

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "gamer/TetMesh.h"

/// Namespace for all things gamer
namespace gamer
{

namespace py = pybind11;


void init_TMCell(py::module& mod){
    py::class_<TMCell> cell(mod, "Cell",
        R"delim(
            Wrapper around a :cpp:class:`gamer::TMCell`.
        )delim"
    );
    cell.def(py::init<>(), "Default constructor");
    cell.def(py::init<int, bool>(), "Construct with marker and selection");
    cell.def(py::init<int, int, bool>(), "Construct with orientation, marker, and selection");
    cell.def_readwrite("orientation", &TMCell::orientation, "The orientation of the cell");
    cell.def_readwrite("marker", &TMCell::marker, "Boundary marker value");
    cell.def_readwrite("selected", &TMCell::selected, "Selection status of cell");
    cell.def("__repr__", &TMCell::to_string, "Pretty print");
}

} // end namespace gamer
