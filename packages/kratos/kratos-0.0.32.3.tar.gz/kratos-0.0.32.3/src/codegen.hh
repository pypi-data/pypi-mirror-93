#ifndef KRATOS_CODEGEN_HH
#define KRATOS_CODEGEN_HH

#include <sstream>

#include "context.hh"
#include "ir.hh"
#include "pass.hh"

namespace kratos {

class SystemVerilogCodeGen;

using DebugInfo = std::map<uint32_t, std::vector<std::pair<std::string, uint32_t>>>;

class VerilogModule {
public:
    explicit VerilogModule(Generator* generator) : generator_(generator) {
        manager_.register_builtin_passes();
    }

    void run_passes();

    [[nodiscard]] std::map<std::string, std::string> verilog_src();
    inline PassManager& pass_manager() { return manager_; }

private:
    Generator* generator_;

    PassManager manager_;
};

class Stream : public std::stringstream {
public:
    explicit Stream(Generator* generator, SystemVerilogCodeGen* codegen);
    Stream& operator<<(AssignStmt* stmt);
    Stream& operator<<(const std::pair<Port*, std::string>& port);
    Stream& operator<<(const std::shared_ptr<Var>& var);

    static std::string get_var_decl(Var* var);

    inline char endl() {
        line_no_++;
        return '\n';
    }

    inline uint32_t line_no() const { return line_no_; }

private:
    Generator* generator_;
    SystemVerilogCodeGen* codegen_;
    uint64_t line_no_;
};

class SystemVerilogCodeGen {
public:
    explicit SystemVerilogCodeGen(Generator* generator);
    SystemVerilogCodeGen(Generator* generator, std::string package_name, std::string header_name);

    inline std::string str() {
        output_module_def(generator_);
        return stream_.str();
    }

    uint32_t indent_size = 2;

    std::string indent();
    void increase_indent() { indent_++; }
    void decrease_indent() { indent_--; }

    // helper function
    std::string static get_port_str(Port* port);
    static std::string get_var_width_str(const Var* var);
    static std::string get_width_str(uint32_t width);
    static std::string get_width_str(Var *var);
    static std::string enum_code(Enum* enum_);

private:
    uint32_t indent_ = 0;
    Generator* generator_;
    bool skip_indent_ = false;
    std::unordered_map<StmtBlock*, std::string> label_index_;
    std::string package_name_;
    std::string header_include_name_;

    // for yosys generate src
    bool yosys_src_ = false;

protected:
    Stream stream_;
    void generate_ports(Generator* generator);
    void generate_variables(Generator* generator);
    void generate_parameters(Generator* generator);
    void generate_functions(Generator* generator);

    virtual void dispatch_node(IRNode* node);

    virtual void stmt_code(AssignStmt* stmt);

    void stmt_code(ReturnStmt* stmt);

    void stmt_code(StmtBlock* stmt);

    void stmt_code(SequentialStmtBlock* stmt);

    void stmt_code(CombinationalStmtBlock* stmt);

    void stmt_code(ScopedStmtBlock* stmt);

    void stmt_code(IfStmt* stmt);

    void stmt_code(ModuleInstantiationStmt* stmt);

    void stmt_code(InterfaceInstantiationStmt* stmt);

    void stmt_code(SwitchStmt* stmt);

    void stmt_code(FunctionStmtBlock* stmt);

    void stmt_code(InitialStmtBlock* stmt);

    void stmt_code(FunctionCallStmt* stmt);

    void stmt_code(AssertBase* stmt);

    void stmt_code(CommentStmt* stmt);

    void stmt_code(RawStringStmt* stmt);

    void stmt_code(AssertPropertyStmt* stmt);

    void stmt_code(ForStmt* stmt);

    void stmt_code(LatchStmtBlock *stmt);

    void enum_code_(Enum* enum_);
    static void enum_code_(Stream& stream_, Enum* enum_, bool debug);
    void generate_enums(kratos::Generator* generator);

    // reverse indexing the named blocks
    std::unordered_map<StmtBlock*, std::string> index_named_block();
    std::string block_label(StmtBlock* stmt);

    // the actual code gen part
    void output_module_def(Generator* generator);

    // raw package imports
    void generate_module_package_import(Generator* generator);

    // code gen port interface
    void generate_port_interface(InstantiationStmt* stmt);
    void generate_interface(Generator* generator);

    // shared code gen blocks
    void block_code(const std::string& syntax_name, StmtBlock* stmt);

private:
    void check_yosys_src();
    void output_yosys_src(IRNode *node);
};

std::string create_stub(Generator* top);

// useful to tools that doesn't support N-D array
Generator& create_wrapper_flatten(Generator* top, const std::string& wrapper_name);

std::pair<std::string, uint32_t> generate_sv_package_header(Generator* top,
                                                            const std::string& package_name,
                                                            bool include_guard);

void fix_verilog_ln(Generator* generator, uint32_t offset);

}  // namespace kratos
#endif  // KRATOS_CODEGEN_HH
