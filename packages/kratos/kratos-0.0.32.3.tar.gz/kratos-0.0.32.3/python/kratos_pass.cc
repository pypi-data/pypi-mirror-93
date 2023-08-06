#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "../src/debug.hh"
#include "../src/except.hh"
#include "../src/expr.hh"
#include "../src/generator.hh"
#include "../src/pass.hh"
#include "../src/stmt.hh"
#include "kratos_expr.hh"

namespace py = pybind11;
using std::shared_ptr;
using namespace kratos;

// pass submodule
void init_pass(py::module &m) {
    auto pass_m = m.def_submodule("passes");

    pass_m.def("fix_assignment_type", &fix_assignment_type)
        .def("remove_unused_vars", &remove_unused_vars)
        .def("verify_generator_connectivity", &verify_generator_connectivity)
        .def("create_module_instantiation", &create_module_instantiation)
        .def("hash_generators", &hash_generators)
        .def("hash_generators_parallel", &hash_generators_parallel)
        .def("hash_generators_sequential", &hash_generators_sequential)
        .def("decouple_generator_ports", &decouple_generator_ports)
        .def("uniquify_generators", &uniquify_generators)
        .def("generate_verilog", py::overload_cast<Generator *>(&generate_verilog))
        .def("generate_verilog",
             py::overload_cast<Generator *, const std::string &, const std::string &, bool>(
                 &generate_verilog))
        .def("generate_verilog", py::overload_cast<Generator *>(&generate_verilog))
        .def("transform_if_to_case", &transform_if_to_case)
        .def("remove_fanout_one_wires", &remove_fanout_one_wires)
        .def("remove_pass_through_modules", &remove_pass_through_modules)
        .def("extract_debug_info", &extract_debug_info)
        .def("compute_enable_condition", &compute_enable_condition)
        .def("extract_struct_info", &extract_struct_info)
        .def("extract_enum_info", &extract_enum_info)
        .def("merge_wire_assignments", merge_wire_assignments)
        .def("zero_out_stubs", &zero_out_stubs)
        .def("remove_unused_stmts", &remove_unused_stmts)
        .def("check_mixed_assignment", &check_mixed_assignment)
        .def("zero_generator_inputs", &zero_generator_inputs)
        .def("insert_pipeline_stages", &insert_pipeline_stages)
        .def("change_port_bundle_struct", &change_port_bundle_struct)
        .def("realize_fsm", &realize_fsm)
        .def("check_function_return", &check_function_return)
        .def("sort_stmts", &sort_stmts)
        .def("check_active_high", &check_active_high)
        .def("extract_dpi_function", &extract_dpi_function)
        .def("extract_interface_info", &extract_interface_info)
        .def("extract_debug_break_points", &extract_debug_break_points)
        .def("insert_verilator_public", &insert_verilator_public)
        .def("remove_assertion", &remove_assertion)
        .def("check_inferred_latch", &check_inferred_latch)
        .def("check_multiple_driver", &check_multiple_driver)
        .def("check_flip_flop_always_ff", &check_flip_flop_always_ff)
        .def("check_combinational_loop", &check_combinational_loop)
        .def("merge_if_block", &merge_if_block)
        .def("find_driver_signal", &find_driver_signal)
        .def("extract_register_names", &extract_register_names)
        .def("extract_var_names", &extract_var_names)
        .def("auto_insert_clock_enable", &auto_insert_clock_enable)
        .def("auto_insert_sync_reset", &auto_insert_sync_reset)
        .def("change_property_into_stmt", &change_property_into_stmt);

    auto manager = py::class_<PassManager>(pass_m, "PassManager", R"pbdoc(
This class gives you the fined control over which pass to run and in which order.
Most passes doesn't return anything, thus it's safe to put it in the pass manager and
let is run. However, if you want to code gen verilog, you have to call generate_verilog()
by yourself to obtain the verilog code.)pbdoc");
    manager.def(py::init<>())
        .def("register_pass",
             py::overload_cast<const std::string &, std::function<void(Generator *)>>(
                 &PassManager::register_pass))
        .def("run_passes", &PassManager::run_passes)
        .def("add_pass", &PassManager::add_pass)
        .def("has_pass", &PassManager::has_pass);

    // trampoline class for ast visitor
    class PyIRVisitor : public IRVisitor {
    public:
        using IRVisitor::IRVisitor;

        void visit_root(IRNode *root) override {
            PYBIND11_OVERLOAD(void, IRVisitor, visit_root, root);
        }

        void visit_generator_root(Generator *generator) override {
            PYBIND11_OVERLOAD(void, IRVisitor, visit_generator_root, generator);
        }

        void visit_content(Generator *generator) override {
            PYBIND11_OVERLOAD(void, IRVisitor, visit_content, generator);
        }

        void visit(AssignStmt *stmt) override { PYBIND11_OVERLOAD(void, IRVisitor, visit, stmt); }

        void visit(Port *var) override { PYBIND11_OVERLOAD(void, IRVisitor, visit, var); }

        void visit(Generator *generator) override {
            PYBIND11_OVERLOAD(void, IRVisitor, visit, generator);
        }

        void visit(Var *var) override { PYBIND11_OVERLOAD(void, IRVisitor, visit, var); }

        void visit(VarSlice *slice) override { PYBIND11_OVERLOAD(void, IRVisitor, visit, slice); }

        void visit(VarVarSlice *slice) override {
            PYBIND11_OVERLOAD(void, IRVisitor, visit, slice);
        }
    };

    auto ast_visitor = py::class_<IRVisitor, PyIRVisitor>(pass_m, "IRVisitor");
    ast_visitor.def(py::init<>())
        .def("visit_generator", py::overload_cast<Generator *>(&IRVisitor::visit))
        .def("visit_root", &IRVisitor::visit_root);

    auto ast = py::class_<IRNode, std::shared_ptr<IRNode>>(pass_m, "IRNode");
    ast.def(py::init<IRNodeKind>());
    def_attributes<py::class_<IRNode, std::shared_ptr<IRNode>>, IRNode>(ast);

    // attributes
    // type holder due to conversion
    class PyAttribute : public Attribute {
    public:
        explicit PyAttribute(py::object target) : Attribute(), target_(std::move(target)) {
            type_str = "python";
        }

    public:
        using Attribute::Attribute;

        py::object get_py_obj() { return target_; }

        static PyAttribute create(const py::object &target) { return PyAttribute(target); }
        static PyAttribute create_attr(const std::string &value) {
            auto r = PyAttribute(py::str(value));
            r.value_str = value;
            return r;
        }

    private:
        py::object target_ = py::none();
    };

    auto attribute =
        py::class_<Attribute, PyAttribute, std::shared_ptr<Attribute>>(pass_m, "Attribute");
    attribute.def(py::init(&PyAttribute::create))
        .def_readwrite("type_str", &PyAttribute::type_str)
        .def("get", [=](PyAttribute &attr) { return attr.get_py_obj(); })
        .def_readwrite("value_str", &PyAttribute::value_str)
        .def_static("create", &PyAttribute::create_attr);
    py::implicitly_convertible<Attribute, PyAttribute>();

    m.def("create_stub", &create_stub);
}

template <typename T>
constexpr void add_cast_type(py::module &m, const std::string &name) {
    m.def(("cast_" + name).c_str(), [](IRNode *node) -> T * {
        auto result = dynamic_cast<T *>(node);
        return result;
    });
}

void init_cast(py::module &m) {
    auto cast_m = m.def_submodule("cast");

    add_cast_type<Var>(cast_m, "var");
    add_cast_type<Port>(cast_m, "port");
    add_cast_type<Const>(cast_m, "const");
    add_cast_type<Generator>(cast_m, "generator");
    add_cast_type<VarSlice>(cast_m, "var_slice");
    add_cast_type<VarVarSlice>(cast_m, "var_var_slice");
    add_cast_type<Expr>(cast_m, "expr");
    add_cast_type<ConditionalExpr>(cast_m, "conditional_expr");
    add_cast_type<Stmt>(cast_m, "stmt");
    add_cast_type<IfStmt>(cast_m, "if_stmt");
    add_cast_type<SwitchStmt>(cast_m, "switch_stmt");
    add_cast_type<StmtBlock>(cast_m, "stmt_block");
    add_cast_type<AssignStmt>(cast_m, "assign_stmt");
}