#ifndef KRATOS_INTERFACE_HH
#define KRATOS_INTERFACE_HH

#include "expr.hh"
#include "port.hh"

namespace kratos {

struct IDefinition {
public:
    using InterfacePortDef = std::tuple<uint32_t, std::vector<uint32_t>, PortDirection, PortType>;
    using InterfaceVarDef = std::pair<uint32_t, std::vector<uint32_t>>;
    [[nodiscard]] virtual bool has_port(const std::string &name) const = 0;
    [[nodiscard]] virtual bool has_var(const std::string &name) const = 0;

    [[nodiscard]] virtual IDefinition::InterfacePortDef port(const std::string &name) const = 0;
    [[nodiscard]] virtual IDefinition::InterfaceVarDef var(const std::string &name) const = 0;

    [[nodiscard]] virtual std::set<std::string> ports() const = 0;
    [[nodiscard]] virtual std::set<std::string> vars() const = 0;

    [[nodiscard]] virtual const std::string &name() const = 0;
    [[nodiscard]] virtual std::string def_name() const = 0;

    [[nodiscard]] virtual bool is_modport() const { return false; }

    virtual ~IDefinition() = default;
};

struct InterfaceDefinition : public IDefinition {
public:
    explicit InterfaceDefinition(std::string name) : name_(std::move(name)) {}

    std::shared_ptr<InterfaceModPortDefinition> create_modport_def(const std::string &name);

    std::string port(const std::string &name, uint32_t width, uint32_t size, PortDirection dir);
    std::string port(const std::string &name, uint32_t width, const std::vector<uint32_t> &size,
                     PortDirection dir);
    std::string port(const std::string &name, uint32_t width, const std::vector<uint32_t> &size,
                     PortDirection dir, PortType type);
    std::string clock(const std::string &name) {
        return port(name, 1, {1}, PortDirection::In, PortType::Clock);
    }
    std::string reset(const std::string &name) {
        return port(name, 1, {1}, PortDirection::In, PortType::AsyncReset);
    }
    std::string input(const std::string &name, uint32_t width, uint32_t size);
    std::string output(const std::string &name, uint32_t width, uint32_t size);
    std::string var(const std::string &name, uint32_t width) { return var(name, width, 1); }
    std::string var(const std::string &name, uint32_t width, uint32_t size);
    std::string var(const std::string &name, uint32_t width, const std::vector<uint32_t> &size);

    [[nodiscard]] bool has_port(const std::string &name) const override;
    [[nodiscard]] bool has_var(const std::string &name) const override;

    [[nodiscard]] IDefinition::InterfacePortDef port(const std::string &name) const override;
    [[nodiscard]] IDefinition::InterfaceVarDef var(const std::string &name) const override;

    [[nodiscard]] std::set<std::string> ports() const override;
    [[nodiscard]] std::set<std::string> vars() const override;

    [[nodiscard]] const std::string &name() const override { return name_; }
    [[nodiscard]] std::string def_name() const override { return name_; }

    [[nodiscard]] const std::map<std::string, std::shared_ptr<InterfaceModPortDefinition>>
        &mod_ports() const {
        return mod_ports_;
    }

private:
    std::string name_;
    std::map<std::string, IDefinition::InterfacePortDef> ports_;
    std::map<std::string, IDefinition::InterfaceVarDef> vars_;
    std::map<std::string, std::shared_ptr<InterfaceModPortDefinition>> mod_ports_;
};

struct InterfaceModPortDefinition : public IDefinition {
public:
    InterfaceModPortDefinition(InterfaceDefinition *def, std::string name);
    void set_input(const std::string &name);
    void set_output(const std::string &name);

    [[nodiscard]] bool has_port(const std::string &name) const override {
        return inputs_.find(name) != inputs_.end() || outputs_.find(name) != outputs_.end();
    }
    [[nodiscard]] bool has_var(const std::string &) const override { return false; }

    [[nodiscard]] IDefinition::InterfacePortDef port(const std::string &name) const override;
    [[nodiscard]] IDefinition::InterfaceVarDef var(const std::string &name) const override;

    [[nodiscard]] std::set<std::string> ports() const override;
    [[nodiscard]] std::set<std::string> vars() const override;

    [[nodiscard]] const std::set<std::string> &inputs() const { return inputs_; }
    [[nodiscard]] const std::set<std::string> &outputs() const { return outputs_; }

    [[nodiscard]] const InterfaceDefinition *def() const { return def_; }
    [[nodiscard]] const std::string &name() const override { return name_; }
    [[nodiscard]] std::string def_name() const override;

    [[nodiscard]] bool is_modport() const override { return true; }

private:
    InterfaceDefinition *def_;
    std::string name_;

    std::set<std::string> inputs_;
    std::set<std::string> outputs_;
};

struct InterfaceRef {
public:
    explicit InterfaceRef(std::shared_ptr<IDefinition> instance, Generator *gen, std::string name)
        : definition_(std::move(instance)), gen_(gen), name_(std::move(name)) {}
    Var &var(const std::string &name) const;
    Port &port(const std::string &name) const;
    void var(const std::string &name, Var *var) { vars_.emplace(name, var); }
    void port(const std::string &name, Port *port) { ports_.emplace(name, port); }
    [[nodiscard]] const std::unordered_map<std::string, Var *> &vars() const { return vars_; }
    [[nodiscard]] const std::unordered_map<std::string, Port *> &ports() const { return ports_; }

    [[nodiscard]] inline bool has_var(const std::string &name) const {
        return vars_.find(name) != vars_.end();
    }
    [[nodiscard]] inline bool has_port(const std::string &name) const {
        return ports_.find(name) != ports_.end();
    }

    bool &is_port() { return is_port_; }
    bool is_port() const { return is_port_; }

    [[nodiscard]] Generator *gen() const { return gen_; }
    [[nodiscard]] const std::string &name() const { return name_; }
    [[nodiscard]] std::string base_name() const;
    [[nodiscard]] bool has_instantiated() const { return has_instantiated_; }
    bool &has_instantiated() { return has_instantiated_; }
    [[nodiscard]] const std::shared_ptr<IDefinition> &definition() const { return definition_; }

    std::shared_ptr<InterfaceRef> get_modport_ref(const std::string &name);
    bool has_modport(const std::string &name);

private:
    std::shared_ptr<IDefinition> definition_;
    std::unordered_map<std::string, Var *> vars_;
    std::unordered_map<std::string, Port *> ports_;

    bool is_port_ = false;
    Generator *gen_;
    std::string name_;

    bool has_instantiated_ = false;

    std::unordered_map<std::string, std::shared_ptr<InterfaceRef>> mod_ports_;
    // only used for modport logic
    std::unordered_map<std::string, std::shared_ptr<ModportPort>> modport_ports_;

    InterfaceRef* interface_parent_ = nullptr;
};

}  // namespace kratos

#endif  // KRATOS_INTERFACE_HH
