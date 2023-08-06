/**
 * Module for handling the NETCONF controls
 */
let netconf = function() {

    let config = {
        /* store public configurations here */
        moduleSelect: '#ytool-models',
        yangsetSelect: '#ytool-yangset',
        protoOpSelect: '#ys-proto-op',
        datastoreGroup: "#ys-datastore-group",
        datastoreGroupButtons: "#ys-datastore-group .btn",
        progressBar: "div#ys-progress",
        selectedDevice: "#ys-devices-rpc",
        selectedDsstore: "#ys-target",
        retryTimer: "#ys-retry-timer",
        lockButton: "#ys-btn-lock span",
        lockTogglePrefix: "#ys-toggle-lock-",
        startSession: "button#ys-session-toggle",
        sessionStatusElem: null,
        lockUnlockDialog: "div#ys-lockunlock-dialog",
        lockSetURI: "/netconf/lock/set/",
        sessionStartEndURI: "/netconf/session/start_end/",
        lockCheckURI: "/netconf/lock/check/",
        selectedDeviceChanged: false,
        deviceDatastoreCache: {},
    };

    function getProtocolOperation() {
        return ($(config.protoOpSelect).val() ||
                $(config.protoOpSelect).attr('data-value'));
    }

    /**
     * Creates the netconf config mode pulldown menu in a tree cell.
     *
     * If a node is a key or is mandatory, you should not be able to
     * delete it directly, however, if the node is a container, the intent
     * is to delete all resources in its subtree which is ok.  A container
     * is flagged as mandatory if any of its children are mandatory.
     *
     * @param {Object} node representing a YANG leaf, container, etc...
     */
    function buildEditProtocolOperationMenu(node) {
        let data = node.data;
        let edit_ops = ["merge", "delete", "replace", "create", "remove"];
        let target = $('<select class="ytool-edit-op" nodeid="'+node.id+'">');

        $.each(edit_ops, function(i, op) {
            if ((op == 'delete' || op == 'remove') &&
                (node.data.key == 'true' ||
                    (node.data.mandatory == 'true' &&
                     node.data.nodetype != 'container'))) {
                return true;
            }
            target.append('<option>'+op+'</option>');
        });
        target.append('</select>');
        return target;
    }

    /**
     * Refresh "NETCONF operation" button bar based on the
     * NETCONF global operations allowed/supported for the loaded YANG module(s)
     */
    function refreshProtocolOperationInputs() {
        let target = $("#ys-proto-op");
        let selection = ($(config.protoOpSelect).val() ||
                         $(config.protoOpSelect).attr('data-value'));

        // Disable all options to start with
        target.find("option, .btn").prop("disabled", true);

        let tree = $("#tree").jstree(true);
        // Iterate over top-level (module) nodes
        $.each(tree.get_node('#').children, function(i, id) {
            let node = tree.get_node(id);
            $.each(node.data.operations, function(i, op) {
                let option = target.find("#netconf-op-" + op);
                option.prop("disabled", false);
            });
        });

        // If previous selection is no longer active, change it to the
        // first available option.
        if (target.find('#netconf-op-' + selection).hasClass("disabled")) {
            let first = target.find('.btn:not(.disabled):first, ' +
                                    'option:not(.disabled):first');
            selection = first.val() || first.attr('data-value');
        }
        $('#ys-proto-op').val(selection).change();
    }

    /**
     * Refresh 'Datastore' options based on the selected device and NETCONF operation.
     */
    function refreshDatastores() {
        let proto_op = ($(config.protoOpSelect).val() ||
                        $(config.protoOpSelect).attr('data-value'));

        let dsmenu = $(config.datastoreGroup);
        let selection = dsmenu.find(".btn.selected").attr('data-value');

        $(config.datastoreGroupButtons).removeClass("selected");
        $(config.datastoreGroupButtons).addClass("disabled");

        for (let dsstore of config.deviceDatastoreCache[proto_op]) {
            let btn = dsmenu.find(".datastore-" + dsstore);
            btn.removeClass("disabled");
        }
        // If previous selection is no longer active, change to the first
        // available option.
        if (dsmenu.find('.datastore-' + selection).hasClass("disabled")) {
           let first = dsmenu.find(".btn:not(.disabled):first");
           selection = first.attr("data-value");
        }
        dsmenu.find('.datastore-' + selection).click();
    }



    /**
     * Based on the selected proto-op, show all nodes in the jstree grid that
     * are capable of this operation, and disable or hide all others.
     *
     * As iterating over the entire tree may be time-consuming (e.g. with
     * large models like Cisco-IOS-XE-native), we only filter the visible nodes.
     */
    function filterNodes() {
        let proto_op = ($(config.protoOpSelect).val() ||
                        $(config.protoOpSelect).attr('data-value'));
        let tree = $("#tree").jstree(true);
        let hide_disabled_nodes = $('input[name="hide-nodes"]:checked').val();

        let visible_node_elems = $("#tree").find("li.jstree-node").toArray();

        for (let node_elem of visible_node_elems) {
            let node = tree.get_node(node_elem.id);
            filterNode(node, tree, proto_op, (hide_disabled_nodes == 'hide'));
        }
        tree.redraw();
    }

    /**
     * Based on the given proto-op, show, hide, or disable the given node.
     *
     * @param {Object} node: jstree node
     * @param {Object} tree: jstree instance
     * @param {string} proto_op: Protocol operation - edit-config, get, etc.
     * @param {boolean} hide_disabled_nodes
     */
    function filterNode(node, tree, proto_op, hide_disabled_nodes) {
        let enable = false;
        /*
         * 'choice' and 'case' nodes have no applicable operations,
         * but share the visibility of their parent/child nodes.
         * We can just show/enable them unconditionally, as if their
         * parents are hidden, they will remain hidden regardless.
         */
        if (node.data.nodetype == 'case' ||
            node.data.nodetype == 'choice') {
            enable = true;
        }
        for (let p in node.data.operations) {
            let op = node.data.operations[p];
            /*
             * 'input' and 'output' are subtrees of a rpc. They're not
             * considered separate module-level operations, so show them
             * if we're looking for an RPC.
             *
             * Similarly, when dealing with 'action', allow inputs and outputs,
             * and also enable list keys in the path to the action.
             */
            if (op == proto_op ||
                (proto_op == 'rpc' && (op == 'input' || op == 'output')) ||
                (proto_op == 'action' && (op == 'input' ||
                                          op == 'output' ||
                                          node.data.key))) {
                enable = true;
                break;
            }
        }

        if (node.data.deviation == 'not-supported') {
            enable = false;
        }

        if (enable) {
            tree.enable_node(node);
            tree.show_node(node, skip_redraw=true);
        } else {
            tree.disable_node(node);
            /*
             * To reduce user consternation, never hide root (module)
             * nodes, even if disabled
             */
            if (hide_disabled_nodes && node.parent != "#") {
                tree.hide_node(node, skip_redraw=true);
            } else {
                tree.show_node(node, skip_redraw=true);
            }
        }
    }

    function jsTree(pth, names, yangset) {
        return rpc_ui.makeJSTreeGrid(names, yangset).then(function() {
            $(yangtree.config.tree).bind('loaded_grid.jstree', filterNodes);
            $(yangtree.config.tree).bind('loaded_grid.jstree',
                                       refreshProtocolOperationInputs);
            $(yangtree.config.tree).bind('after_open.jstree', function(e, data) {
                let tree = data.instance;
                let node = data.node;
                let hide_disabled_nodes = $('input[name="hide-nodes"]:checked').val();
                let proto_op = ($(config.protoOpSelect).val() ||
                                $(config.protoOpSelect).attr('data-value'));
                // Enable/disable/show/hide the revealed nodes as appropriate
                $.each(tree.get_children_dom(node), function(i, node_elem) {
                    filterNode(tree.get_node(node_elem.id), tree,
                               proto_op, (hide_disabled_nodes == 'hide'));
                });
            });
        });
    }

    /**
     * Public APIs
     */

    /**
    * Function to Lock/Unlock the datastore
    */
    function lockUnlockDatastore(lock, device, dsstore) {
        let data = {
            lock: lock,
            device: device,
            dsstore: dsstore,
        };
        data['retry_timer'] = $(config.retryTimer).val() || '45';
        $.when(jsonPromise(config.lockSetURI, data))
            .then(function(retObj) {
                // Check the message as we don't have a status flag - yuck
                if (retObj.resp == 'Datastore Locked' ||
                    retObj.resp == 'Datastore unlocked successfully' ||
                    retObj.resp == 'Already Unlocked') {
                    toggleLockButton(dsstore, lock);
                } else {
                    popDialog('Error: ' + retObj.resp);
                }
            }, function(retObj) {
                popDialog('Error' + retObj.status + ':' + retObj.statusText);
            });
    };

    /**
     * UI helper for lockUnlockDatastore
     */
    function toggleLockButton(dsstore, lock) {
        let btn = $(config.lockTogglePrefix + dsstore);
        let lockElem = btn.find('.icon');
        if (lock) {
            lockElem.removeClass("icon-unlock");
            lockElem.addClass("icon-lock");
            btn.addClass("btn--negative");
        } else {
            lockElem.removeClass("icon-lock");
            lockElem.addClass("icon-unlock");
            btn.removeClass("btn--negative");
        }
    };

    /**
     * UI helper for startEndSession
     *
     * @param {boolean} state - Is a session in progress?
     */
    function toggleSessionButton(state) {
        if (state) {
            $(config.startSession).text("End Session");
            $(config.startSession).removeClass("btn--primary");
            $(config.startSession).addClass("btn--negative");
            if (config.sessionStatusElem) {
                $(config.sessionStatusElem).text(
                    $(config.sessionStatusElem).text().replace("(not connected)",
                                                               "(connected)")
                );
            }
        } else {
            $(config.startSession).text("Start Session");
            $(config.startSession).removeClass("btn--negative");
            $(config.startSession).addClass("btn--primary");
            /* No locks when no session is in progress */
            for (let ds of ['candidate', 'running', 'startup']) {
                toggleLockButton(ds, false);
            }
            if (config.sessionStatusElem) {
                $(config.sessionStatusElem).text(
                    $(config.sessionStatusElem).text().replace("(connected)",
                                                               "(not connected)")
                );
            }
        }
    };

    /**
     * Function to start or end a netconf session.
     *
     * @param {string} device - Slug identifying the device profile of interest
     * @param {string} action - one of 'start', 'end'
     */
    function startEndSession(device, action) {
        let data = {
            device: device,
            session: action
        };
        if (action == 'start') {
            $(config.startSession).text("Starting Session...");
        } else {
            $(config.startSession).text("Ending Session...");
        }
        return $.when(jsonPromise(config.sessionStartEndURI, data))
            .then(function(retObj) {
                if (retObj.reply) {
                    // successful outcome
                    toggleSessionButton(action == 'start');
                } else {
                    // something went wrong - reset button to prior state
                    toggleSessionButton(action != 'start');
                }
            }, function(retObj) {
                popDialog('Error' + retObj.status + ':' + retObj.statusText);
            });
    };

    /**
     * Function to retrieve a set of all supported datastores from a device.
     * @param {string} device - Slug identifying the device profile of interest
     */
    function getAllDatastores(device) {
        return $.ajax({
            url: '/netconf/datastores',
            type: 'GET',
            data: {
                device: device,
                list_all: true,
            },
            dataType: 'json',
            error: function(data) {
                popDialog("Error " + data.status + ": " + data.statusText);
                $(config.datastoreGroupButtons).removeClass("disabled");
            }
        });
    }
    /**
     * Function to retrieve a mapping of operations to datastores from a device.
     */
    function getDatastores() {
        let proto_op = ($(config.protoOpSelect).val() ||
                        $(config.protoOpSelect).attr('data-value'));
        let device = $('select.ys-devices').val();

        if (!proto_op || !device) {
            // Default to all possible datastores until the user selects something
            $(config.datastoreGroupButtons).removeClass("disabled");
            return;
        }
        if (!config.selectedDeviceChanged) {
            refreshDatastores();
            return;
        }

        let progressBarText = "Device loading...";
        let progressBarDiv = startProgress($(config.progressBar),"","",progressBarText) || $(config.progressBar);

        $.ajax({
            url: '/netconf/datastores',
            type: 'GET',
            data: {
                device: device
            },
            dataType: 'json',
            success: function(data) {
                config.deviceDatastoreCache = data;
                config.selectedDeviceChanged = false;
                refreshDatastores();
                stopProgress(progressBarDiv);
            },
            error: function(data) {
                popDialog("Error " + data.status + ": " + data.statusText);
                $(config.datastoreGroupButtons).removeClass("disabled");
                stopProgress(progressBarDiv);
            }
        });
    };

    /**
     * Function to retrieve the NETCONF capabilities reported by a device.
     */
    function getCapabilities(device) {
        return $.ajax({
            url: '/netconf/capabilities',
            type: 'GET',
            data: {
                device: device,
            },
            dataType: 'json',
        });
    }

    /**
     * Function to set logging levels for ncclient operations.
     */
    function setLoggingLevel() {
        let loglevel = 'informational';
        if ($("#ys-logging").is(":checked")) {
            loglevel = 'debug';
        }
        $.when(getPromise('/netconf/setlog/', {"loglevel": loglevel}))
            .then(function(retObj) {
                if (retObj.reply) {
                    popDialog("NETCONF logging set to "+ loglevel.toUpperCase() +" level");
                }
            }, function(retObj) {
                popDialog('Error' + retObj.status + ':' + retObj.statusText);
            });
    }

    /**
     * Given an XPath containing list key predicates,
     * return the list of (xpath, value) tuples needed to construct this XPath.
     *
     * Something of an inverse of rpc_ui.updateListKeyXPaths.
     *
     * Given an XPath like
     * /listA[keyA="valueA"]/listB[keyB1="1"][keyB2="2"]/leaf,
     * we will return:
     * [
     *   ['/listA/keyA', 'valueA'],
     *   ['/listA[keyA="valueA"]/listB/keyB1', '1'],
     *   ['/listA[keyA="valueA"]/listB[keyB1="1"]/keyB2', '2'],
     * ]
     *
     * As in updateListKeyXPaths, we need to also handle cases like
     *   /list[key='"hello"']/
     *   /list[key=concat('he said "', "I said 'hello!'", '" again')]
     *
     * Whee!
     */
    function decomposeXPathListKeys(xpath) {
        pfx = xpath.split(":")[0]+":"
        let result = [];

        singleQuotedValue = new RegExp("^\\[([^=]+)='([^']*)'\\]");
        doubleQuotedValue = new RegExp('^\\[([^=]+)="([^"]*)"\\]');
        concatValue = new RegExp(`^\\[([^=]+)=concat\\(` +
                                 `(?:"([^"]*)"|'([^']*)')` +
                                 `(?: *, *(?:"([^"]*)"|'([^']*)'))*\\)\\]`);


        for (let i = 0; i < xpath.length;) {
            let c = xpath.charAt(i);
            if (c != '[') {
                i++;
                continue;
            }
            prefix = xpath.slice(0, i);
            suffix = xpath.slice(i);
            predicate = (suffix.match(singleQuotedValue) ||
                         suffix.match(doubleQuotedValue) ||
                         suffix.match(concatValue));
            key = predicate[1];
            value = predicate.slice(2).join('');

            leaf_xpath = prefix + pfx + key;
            result.push([leaf_xpath, value]);

            i += predicate[0].length;
        }

        return result;
    };

    /**
     * Helper function to populateReplay(), below - given a replay segment,
     * populate the JSTreeGrid with the contents of the replay.
     */
    function populateJSTreeGrid(segment) {
        rpc_ui.clearGrid();
        if (!segment.yang.modules) {
            popDialog("Custom replay XML cannot be populated into the tree.");
            return;
        }
        let nodes = [];
        // See similar RegExp in rpc_ui.updateXPathSegment
        let stripPredicate = new RegExp(
            `\\[[^\\[\\]]+=("[^"]*"|'[^']*'|` +
                `concat\\((?:"[^"]*"|'[^']*')(?: *, *(?:"[^"]*"|'[^']*'))*\\))\\]`
        );
        let tree = $(yangtree.config.tree).jstree(true);
        for (let module of Object.keys(segment.yang.modules)) {
            for (let cfg of segment.yang.modules[module].configs) {
                let base_xpath = cfg.xpath;
                // Are there any list keys in this XPath? Populate them too
                let xpaths_values = [];
                if (base_xpath.includes('[')) {
                    xpaths_values = decomposeXPathListKeys(base_xpath);
                }
                // Populate the leaf itself, of course!
                xpaths_values.push([cfg.xpath, cfg.value])

                for (let xpath_value_entry of xpaths_values) {
                    xpath = xpath_value_entry[0];
                    value = xpath_value_entry[1];
                    xpath = xpath.replace(stripPredicate, '');
                    // Have to refresh the JSON because XPaths may change
                    // as a result of previous value setting.
                    let treedata = tree.get_json($(yangtree.config.tree),
                                                 {flat: true});
                    for (let node of treedata) {
                        let xpathPfx = undefined;
                        if (node.data.xpath_pfx != undefined) {
                            xpathPfx = node.data.xpath_pfx.replace(stripPredicate, '');
                        }
                        if ( xpathPfx == xpath) {
                            nodes.push(node.id);
                            tree.select_node(node.id);
                            if (value !== undefined) {
                                // TODO: if the node already has a value, we need to add a new list entry
                                // Add the "value" input
                                let gridCell = $("div.jstree-grid-col-1[data-jstreegrid=" + node.id + "]");
                                $(yangtree.config.tree).trigger("select_cell.jstree-grid", {
                                    node: $("li#" + node.id),
                                    column: "Value",
                                    grid: gridCell,
                                });
                                // Set its value appropriately
                                gridCell.find(".ys-cfg-rpc").val(value).change();
                            }
                        }
                    }
                }

                if (cfg["edit-op"] !== undefined) {
                    // Add the "operation" input
                    let treedata = tree.get_json($(yangtree.config.tree),
                                                 {flat: true});
                    for (let node of treedata) {
                        if (node.data.xpath_pfx == cfg.xpath) {
                            let gridCell = $("div.jstree-grid-col-2[data-jstreegrid=" + node.id + "]");
                            $(yangtree.config.tree).trigger("select_cell.jstree-grid", {
                                node: $("li#" + node.id),
                                column: "Operation",
                                grid: gridCell,
                            })
                            // Set its value appropriately
                            gridCell.find(".ytool-edit-op").val(cfg['edit-op']);
                            break;
                        }
                    }
                }
            }
        }
    }

    /**
     * Given structured replay data as returned by tasks.getTask(),
     * populate the UI accordingly, including reloading the jstree if needed,
     * then call rpcmanager.populateSavedRPCsFromReplay, populateJSTreeGrid().
     */
    function populateReplay(taskdata) {
        let progressBarDiv = startProgress($(config.progressBar), "", "",
                                           "Loading replay contents...");
        let modules = [];
        for (let segment of taskdata.task.segments) {
            /* Custom-RPC replays don't have listed modules */
            if (segment.yang.modules) {
                modules = modules.concat(Object.keys(segment.yang.modules));
            }
        }

        /* Sanity check - can we actually display the module(s) required? */
        for (let module of modules) {
            let opt = $(config.moduleSelect).find("option[value=" + module + "]");
            if (opt.length < 1) {
                popDialog('Module "' + module + '" not found in selected YANG set.' +
                          '\nPlease select a YANG set that includes this module.');
                stopProgress(progressBarDiv);
                return;
            }
        }

        rpcmanager.populateSavedRPCsFromReplay(taskdata.task.segments);

        /* Load the required modules, if not already loaded */
        let changedModules = false;
        let selection = $(config.moduleSelect).val() || [];
        for (let module of modules) {
            if (!selection.includes(module)) {
                changedModules = true;
            }
        }

        let lastSegment = taskdata.task.segments[taskdata.task.segments.length - 1];
        if (taskdata.task.segments.length > 1) {
            popDialog("Replay contains multiple segments (RPCs). " +
                      "The JSTree will be populated with the last one.");
            /* keep going, though */
        }
        /* Change the NETCONF operation if necessary */
        let protoOp = lastSegment.yang['proto-op'];
        $(config.protoOpSelect).val(protoOp);

        if (changedModules) {
            $(config.moduleSelect).val(selection.concat(modules));
            $(config.moduleSelect).trigger("chosen:updated");

            /* TODO, the below is similar to code in netconf.html */
            $(".ys-module-required").removeClass("disabled");
            jsTree(['yang'], $(config.moduleSelect).val(),
                   $(config.yangsetSelect).val())
                .then(function() {
                    yangtree.pushExploreState($(config.yangsetSelect).val(),
                                              $(config.moduleSelect).val());
                });

            $(yangtree.config.tree).one('loaded_grid.jstree', function() {
                populateJSTreeGrid(lastSegment);
                stopProgress(progressBarDiv);
            });
        } else {
            populateJSTreeGrid(lastSegment);
            stopProgress(progressBarDiv);
        }
    };

    return {
        config: config,
        jsTree: jsTree,
        getProtocolOperation: getProtocolOperation,
        buildEditProtocolOperationMenu: buildEditProtocolOperationMenu,
        filterNodes: filterNodes,
        getDatastores: getDatastores,
        getAllDatastores: getAllDatastores,
        lockUnlockDatastore: lockUnlockDatastore,
        startEndSession: startEndSession,
        toggleSessionButton: toggleSessionButton,
        getCapabilities: getCapabilities,
        setLoggingLevel: setLoggingLevel,
        decomposeXPathListKeys: decomposeXPathListKeys,
        populateReplay: populateReplay,
    };
}();
