#ifndef KRATOS_PORT_HH
#define KRATOS_PORT_HH

#include <optional>
#include <set>
#include <string>
#include <tuple>
#include <vector>

#include "expr.hh"

namespace kratos {

enum class PortDirection { In, Out, InOut };

enum class PortType { Data, Clock, AsyncReset, Reset, ClockEnable };

struct PackedSlice;

struct Port : public Var {
public:
    Port(Generator *module, PortDirection direction, const std::string &name, uint32_t width,
         uint32_t size, PortType type, bool is_signed);

    Port(Generator *module, PortDirection direction, const std::string &name, uint32_t width,
         const std::vector<uint32_t> &size, PortType type, bool is_signed);

    PortDirection port_direction() const { return direction_; }
    void set_port_direction(PortDirection direction) { direction_ = direction; }
    PortType port_type() const { return type_; }

    virtual void set_port_type(PortType type);

    // AST stuff
    void accept(IRVisitor *visitor) override { visitor->visit(this); }
    uint64_t child_count() override { return 0; }
    IRNode *get_child(uint64_t) override { return nullptr; }

    // coding convention, only valid for width 1 signal
    std::optional<bool> active_high() const { return active_high_; }
    void set_active_high(bool value);

    [[nodiscard]] std::unordered_set<std::shared_ptr<Port>> connected_to() const;
    [[nodiscard]] std::unordered_set<std::shared_ptr<Port>> connected_from() const;

    [[nodiscard]] bool connected() const;

protected:
    std::shared_ptr<AssignStmt> assign_(const std::shared_ptr<Var> &var,
                                        AssignmentType type) override;

private:
    PortDirection direction_;
    PortType type_;

    std::optional<bool> active_high_ = std::nullopt;
};

// diamond virtual inheritance is close to impossible in pybind. duplicate the logic here
struct EnumPort : public Port, public EnumType {
public:
    bool inline is_enum() const override { return true; }

    EnumPort(Generator *m, PortDirection direction, const std::string &name,
             const std::shared_ptr<Enum> &enum_type);

    const inline Enum *enum_type() const override { return enum_type_; }
    void accept(IRVisitor *visitor) override { visitor->visit(this); }

protected:
    std::shared_ptr<AssignStmt> assign_(const std::shared_ptr<Var> &var,
                                        AssignmentType type) override;

private:
    Enum *enum_type_;
};

struct PortPackedStruct : public Port, public PackedInterface {
public:
    PortPackedStruct(Generator *module, PortDirection direction, const std::string &name,
                     PackedStruct packed_struct_);
    PortPackedStruct(Generator *m, PortDirection direction, const std::string &name,
                     PackedStruct packed_struct_, uint32_t size);
    PortPackedStruct(Generator *m, PortDirection direction, const std::string &name,
                     PackedStruct packed_struct_, const std::vector<uint32_t> &size);

    void set_port_type(PortType type) override;

    const PackedStruct &packed_struct() const { return struct_; }

    PackedSlice &operator[](const std::string &member_name);

    // necessary to make pybind happy due to complex inheritance
    VarSlice inline &operator[](std::pair<uint32_t, uint32_t> slice) override {
        return Var::operator[](slice);
    }
    VarSlice inline &operator[](uint32_t idx) override { return Var::operator[](idx); }

    bool is_struct() const override { return true; }

    std::set<std::string> member_names() const override;

    // struct is always packed
    bool is_packed() const override { return true; }
    void set_is_packed(bool value) override;

private:
    PackedStruct struct_;

    void setup_size();
};

struct PortBundleDefinition {
public:
    using PortDef = std::tuple<uint32_t, uint32_t, bool, PortDirection, PortType>;

    void add_definition(const std::string &name, uint32_t width, uint32_t size, bool is_signed,
                        PortDirection direction, PortType type);

    explicit PortBundleDefinition(std::string name) : name_(std::move(name)) {}

    [[nodiscard]] const std::map<std::string, PortDef> &definition() const { return definitions_; }
    [[nodiscard]] const std::map<std::string, std::pair<std::string, uint32_t>> &debug_info()
        const {
        return debug_info_;
    }

    void add_debug_info(const std::string &name, const std::pair<std::string, uint32_t> &info) {
        debug_info_.emplace(name, info);
    }

    void set_name(const std::string &name) { name_ = name; }
    [[nodiscard]] const std::string &get_name() const { return name_; }

    PortBundleDefinition flip();

private:
    std::string name_;
    std::map<std::string, PortDef> definitions_;
    std::map<std::string, PortDef> flipped_definitions_;
    std::map<std::string, std::pair<std::string, uint32_t>> debug_info_;

    PortBundleDefinition() = default;
};

struct PortBundleRef : public PackedInterface {
public:
    PortBundleRef(Generator *generator, PortBundleDefinition def)
        : generator(generator), definition_(std::move(def)) {}

    Port &get_port(const std::string &name);
    void add_name_mapping(const std::string &port_name, const std::string &real_name) {
        name_mappings_.emplace(port_name, real_name);
    }
    [[nodiscard]] const std::map<std::string, std::string> &name_mappings() const {
        return name_mappings_;
    }

    void assign(const std::shared_ptr<PortBundleRef> &other, Generator *parent,
                const std::vector<std::pair<std::string, uint32_t>> &debug_info);

    [[nodiscard]] const std::string &def_name() const { return definition_.get_name(); }

    [[nodiscard]] std::set<std::string> member_names() const override;

private:
    Generator *generator;
    const PortBundleDefinition definition_;
    std::map<std::string, std::string> name_mappings_;
};

struct InterfacePort : public Port {
public:
    InterfacePort(InterfaceRef *interface, Generator *module, PortDirection direction,
                  const std::string &name, uint32_t width, const std::vector<uint32_t> &size,
                  PortType type, bool is_signed)
        : Port(module, direction, name, width, size, type, is_signed), interface_(interface) {}

    std::string to_string() const override;
    std::string base_name() const override;

    bool inline is_interface() const override { return true; };
    const InterfaceRef *interface() const { return interface_; };

private:
    InterfaceRef *interface_ = nullptr;
};

struct ModportPort : public InterfacePort {
    // this is a wrapper around a normal variable to make it looks like a port
public:
    ModportPort(InterfaceRef *ref, Var *var, PortDirection dir);

    // wraps all the critical functions
    const std::unordered_set<std::shared_ptr<AssignStmt>> &sinks() const override {
        return var_->sinks();
    };
    void remove_sink(const std::shared_ptr<AssignStmt> &stmt) override { var_->remove_sink(stmt); }
    const std::unordered_set<std::shared_ptr<AssignStmt>> &sources() const override {
        return var_->sources();
    };
    void clear_sinks(bool remove_parent = false) override { var_->clear_sources(remove_parent); }
    void clear_sources(bool remove_parent = false) override { var_->clear_sinks(remove_parent); }
    void remove_source(const std::shared_ptr<AssignStmt> &stmt) override {
        var_->remove_source(stmt);
    }

    void move_linked_to(Var *new_var) override { var_->move_linked_to(new_var); }
    void add_sink(const std::shared_ptr<AssignStmt> &stmt) override { var_->add_sink(stmt); }
    void add_source(const std::shared_ptr<AssignStmt> &stmt) override { var_->add_source(stmt); }

private:
    Var *var_;
};

}  // namespace kratos

#endif  // KRATOS_PORT_HH
