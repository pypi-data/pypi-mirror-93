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

#include "gamer/SurfaceMesh.h"

/// Namespace for all things gamer
namespace gamer
{

namespace py = pybind11;

void init_SMFace(py::module& mod){
    py::class_<SMFace> face(mod, "Face",
        R"delim(
            Wrapper around a :cpp:class:`gamer::SMFace`.
        )delim"
    );
    face.def(py::init<>(), "Default constructor");
    face.def(py::init<int, bool>(),
        py::arg("marker") = -1,
        py::arg("selected") = false,
        "Construct with marker and selection");
    face.def(py::init<int, int, bool>(),
        py::arg("orientation") = 0,
        py::arg("marker") = -1,
        py::arg("selected") = false,
        "Construct with orientation, marker, and selection");
    face.def_readwrite("orientation", &SMFace::orientation, "The orientation of the face");
    face.def_readwrite("marker", &SMFace::marker, "Boundary marker value");
    face.def_readwrite("selected", &SMFace::selected, "Selection status of face");
    face.def("__repr__", &SMFace::to_string, "Pretty print");
}

} // end namespace gamer
