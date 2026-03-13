import { t as __exportAll } from "./rolldown-runtime-Cbj13DAv.js";
import { c as resolveDefaultAgentId } from "./agent-scope-DWsn5rte.js";
import { p as shouldLogVerbose } from "./subsystem-nlluZawe.js";
import { c as normalizeAgentId, f as sanitizeAgentId, i as buildAgentPeerSessionKey, m as normalizeAccountId, n as DEFAULT_MAIN_KEY, p as DEFAULT_ACCOUNT_ID, r as buildAgentMainSessionKey, t as DEFAULT_AGENT_ID } from "./session-key-a6av96Fj.js";
import { t as logDebug } from "./logger-wD6tEZWm.js";
import { t as normalizeChatType } from "./chat-type-DKb2TlGZ.js";
import { n as listBindings } from "./bindings-CtbdcwyF.js";

//#region src/routing/resolve-route.ts
var resolve_route_exports = /* @__PURE__ */ __exportAll({
	DEFAULT_ACCOUNT_ID: () => DEFAULT_ACCOUNT_ID,
	DEFAULT_AGENT_ID: () => DEFAULT_AGENT_ID,
	buildAgentSessionKey: () => buildAgentSessionKey,
	resolveAgentRoute: () => resolveAgentRoute
});
function normalizeToken(value) {
	return (value ?? "").trim().toLowerCase();
}
function normalizeId(value) {
	if (typeof value === "string") return value.trim();
	if (typeof value === "number" || typeof value === "bigint") return String(value).trim();
	return "";
}
function matchesAccountId(match, actual) {
	const trimmed = (match ?? "").trim();
	if (!trimmed) return actual === DEFAULT_ACCOUNT_ID;
	if (trimmed === "*") return true;
	return normalizeAccountId(trimmed) === actual;
}
function buildAgentSessionKey(params) {
	const channel = normalizeToken(params.channel) || "unknown";
	const peer = params.peer;
	return buildAgentPeerSessionKey({
		agentId: params.agentId,
		mainKey: DEFAULT_MAIN_KEY,
		channel,
		accountId: params.accountId,
		peerKind: peer?.kind ?? "direct",
		peerId: peer ? normalizeId(peer.id) || "unknown" : null,
		dmScope: params.dmScope,
		identityLinks: params.identityLinks
	});
}
function listAgents(cfg) {
	const agents = cfg.agents?.list;
	return Array.isArray(agents) ? agents : [];
}
const agentLookupCacheByCfg = /* @__PURE__ */ new WeakMap();
function resolveAgentLookupCache(cfg) {
	const agentsRef = cfg.agents;
	const existing = agentLookupCacheByCfg.get(cfg);
	if (existing && existing.agentsRef === agentsRef) return existing;
	const byNormalizedId = /* @__PURE__ */ new Map();
	for (const agent of listAgents(cfg)) {
		const rawId = agent.id?.trim();
		if (!rawId) continue;
		byNormalizedId.set(normalizeAgentId(rawId), sanitizeAgentId(rawId));
	}
	const next = {
		agentsRef,
		byNormalizedId,
		fallbackDefaultAgentId: sanitizeAgentId(resolveDefaultAgentId(cfg))
	};
	agentLookupCacheByCfg.set(cfg, next);
	return next;
}
function pickFirstExistingAgentId(cfg, agentId) {
	const lookup = resolveAgentLookupCache(cfg);
	const trimmed = (agentId ?? "").trim();
	if (!trimmed) return lookup.fallbackDefaultAgentId;
	const normalized = normalizeAgentId(trimmed);
	if (lookup.byNormalizedId.size === 0) return sanitizeAgentId(trimmed);
	const resolved = lookup.byNormalizedId.get(normalized);
	if (resolved) return resolved;
	return lookup.fallbackDefaultAgentId;
}
function matchesChannel(match, channel) {
	const key = normalizeToken(match?.channel);
	if (!key) return false;
	return key === channel;
}
const evaluatedBindingsCacheByCfg = /* @__PURE__ */ new WeakMap();
const MAX_EVALUATED_BINDINGS_CACHE_KEYS = 2e3;
const resolvedRouteCacheByCfg = /* @__PURE__ */ new WeakMap();
const MAX_RESOLVED_ROUTE_CACHE_KEYS = 4e3;
function pushToIndexMap(map, key, binding) {
	if (!key) return;
	const existing = map.get(key);
	if (existing) {
		existing.push(binding);
		return;
	}
	map.set(key, [binding]);
}
function peerLookupKeys(kind, id) {
	if (kind === "group") return [`group:${id}`, `channel:${id}`];
	if (kind === "channel") return [`channel:${id}`, `group:${id}`];
	return [`${kind}:${id}`];
}
function collectPeerIndexedBindings(index, peer) {
	if (!peer) return [];
	const out = [];
	const seen = /* @__PURE__ */ new Set();
	for (const key of peerLookupKeys(peer.kind, peer.id)) {
		const matches = index.byPeer.get(key);
		if (!matches) continue;
		for (const match of matches) {
			if (seen.has(match)) continue;
			seen.add(match);
			out.push(match);
		}
	}
	return out;
}
function buildEvaluatedBindingsIndex(bindings) {
	const byPeer = /* @__PURE__ */ new Map();
	const byGuildWithRoles = /* @__PURE__ */ new Map();
	const byGuild = /* @__PURE__ */ new Map();
	const byTeam = /* @__PURE__ */ new Map();
	const byAccount = [];
	const byChannel = [];
	for (const binding of bindings) {
		if (binding.match.peer.state === "valid") {
			for (const key of peerLookupKeys(binding.match.peer.kind, binding.match.peer.id)) pushToIndexMap(byPeer, key, binding);
			continue;
		}
		if (binding.match.guildId && binding.match.roles) {
			pushToIndexMap(byGuildWithRoles, binding.match.guildId, binding);
			continue;
		}
		if (binding.match.guildId && !binding.match.roles) {
			pushToIndexMap(byGuild, binding.match.guildId, binding);
			continue;
		}
		if (binding.match.teamId) {
			pushToIndexMap(byTeam, binding.match.teamId, binding);
			continue;
		}
		if (binding.match.accountPattern !== "*") {
			byAccount.push(binding);
			continue;
		}
		byChannel.push(binding);
	}
	return {
		byPeer,
		byGuildWithRoles,
		byGuild,
		byTeam,
		byAccount,
		byChannel
	};
}
function getEvaluatedBindingsForChannelAccount(cfg, channel, accountId) {
	const bindingsRef = cfg.bindings;
	const existing = evaluatedBindingsCacheByCfg.get(cfg);
	const cache = existing && existing.bindingsRef === bindingsRef ? existing : {
		bindingsRef,
		byChannelAccount: /* @__PURE__ */ new Map(),
		byChannelAccountIndex: /* @__PURE__ */ new Map()
	};
	if (cache !== existing) evaluatedBindingsCacheByCfg.set(cfg, cache);
	const cacheKey = `${channel}\t${accountId}`;
	const hit = cache.byChannelAccount.get(cacheKey);
	if (hit) return hit;
	const evaluated = listBindings(cfg).flatMap((binding) => {
		if (!binding || typeof binding !== "object") return [];
		if (!matchesChannel(binding.match, channel)) return [];
		if (!matchesAccountId(binding.match?.accountId, accountId)) return [];
		return [{
			binding,
			match: normalizeBindingMatch(binding.match)
		}];
	});
	cache.byChannelAccount.set(cacheKey, evaluated);
	cache.byChannelAccountIndex.set(cacheKey, buildEvaluatedBindingsIndex(evaluated));
	if (cache.byChannelAccount.size > MAX_EVALUATED_BINDINGS_CACHE_KEYS) {
		cache.byChannelAccount.clear();
		cache.byChannelAccountIndex.clear();
		cache.byChannelAccount.set(cacheKey, evaluated);
		cache.byChannelAccountIndex.set(cacheKey, buildEvaluatedBindingsIndex(evaluated));
	}
	return evaluated;
}
function getEvaluatedBindingIndexForChannelAccount(cfg, channel, accountId) {
	const bindings = getEvaluatedBindingsForChannelAccount(cfg, channel, accountId);
	const existing = evaluatedBindingsCacheByCfg.get(cfg);
	const cacheKey = `${channel}\t${accountId}`;
	const indexed = existing?.byChannelAccountIndex.get(cacheKey);
	if (indexed) return indexed;
	const built = buildEvaluatedBindingsIndex(bindings);
	existing?.byChannelAccountIndex.set(cacheKey, built);
	return built;
}
function normalizePeerConstraint(peer) {
	if (!peer) return { state: "none" };
	const kind = normalizeChatType(peer.kind);
	const id = normalizeId(peer.id);
	if (!kind || !id) return { state: "invalid" };
	return {
		state: "valid",
		kind,
		id
	};
}
function normalizeBindingMatch(match) {
	const rawRoles = match?.roles;
	return {
		accountPattern: (match?.accountId ?? "").trim(),
		peer: normalizePeerConstraint(match?.peer),
		guildId: normalizeId(match?.guildId) || null,
		teamId: normalizeId(match?.teamId) || null,
		roles: Array.isArray(rawRoles) && rawRoles.length > 0 ? rawRoles : null
	};
}
function resolveRouteCacheForConfig(cfg) {
	const existing = resolvedRouteCacheByCfg.get(cfg);
	if (existing && existing.bindingsRef === cfg.bindings && existing.agentsRef === cfg.agents && existing.sessionRef === cfg.session) return existing.byKey;
	const byKey = /* @__PURE__ */ new Map();
	resolvedRouteCacheByCfg.set(cfg, {
		bindingsRef: cfg.bindings,
		agentsRef: cfg.agents,
		sessionRef: cfg.session,
		byKey
	});
	return byKey;
}
function formatRouteCachePeer(peer) {
	if (!peer || !peer.id) return "-";
	return `${peer.kind}:${peer.id}`;
}
function formatRoleIdsCacheKey(roleIds) {
	const count = roleIds.length;
	if (count === 0) return "-";
	if (count === 1) return roleIds[0] ?? "-";
	if (count === 2) {
		const first = roleIds[0] ?? "";
		const second = roleIds[1] ?? "";
		return first <= second ? `${first},${second}` : `${second},${first}`;
	}
	return roleIds.toSorted().join(",");
}
function buildResolvedRouteCacheKey(params) {
	return `${params.channel}\t${params.accountId}\t${formatRouteCachePeer(params.peer)}\t${formatRouteCachePeer(params.parentPeer)}\t${params.guildId || "-"}\t${params.teamId || "-"}\t${formatRoleIdsCacheKey(params.memberRoleIds)}\t${params.dmScope}`;
}
function hasGuildConstraint(match) {
	return Boolean(match.guildId);
}
function hasTeamConstraint(match) {
	return Boolean(match.teamId);
}
function hasRolesConstraint(match) {
	return Boolean(match.roles);
}
function peerKindMatches(bindingKind, scopeKind) {
	if (bindingKind === scopeKind) return true;
	const both = new Set([bindingKind, scopeKind]);
	return both.has("group") && both.has("channel");
}
function matchesBindingScope(match, scope) {
	if (match.peer.state === "invalid") return false;
	if (match.peer.state === "valid") {
		if (!scope.peer || !peerKindMatches(match.peer.kind, scope.peer.kind) || scope.peer.id !== match.peer.id) return false;
	}
	if (match.guildId && match.guildId !== scope.guildId) return false;
	if (match.teamId && match.teamId !== scope.teamId) return false;
	if (match.roles) {
		for (const role of match.roles) if (scope.memberRoleIds.has(role)) return true;
		return false;
	}
	return true;
}
function resolveAgentRoute(input) {
	const channel = normalizeToken(input.channel);
	const accountId = normalizeAccountId(input.accountId);
	const peer = input.peer ? {
		kind: normalizeChatType(input.peer.kind) ?? input.peer.kind,
		id: normalizeId(input.peer.id)
	} : null;
	const guildId = normalizeId(input.guildId);
	const teamId = normalizeId(input.teamId);
	const memberRoleIds = input.memberRoleIds ?? [];
	const memberRoleIdSet = new Set(memberRoleIds);
	const dmScope = input.cfg.session?.dmScope ?? "main";
	const identityLinks = input.cfg.session?.identityLinks;
	const shouldLogDebug = shouldLogVerbose();
	const parentPeer = input.parentPeer ? {
		kind: normalizeChatType(input.parentPeer.kind) ?? input.parentPeer.kind,
		id: normalizeId(input.parentPeer.id)
	} : null;
	const routeCache = !shouldLogDebug && !identityLinks ? resolveRouteCacheForConfig(input.cfg) : null;
	const routeCacheKey = routeCache ? buildResolvedRouteCacheKey({
		channel,
		accountId,
		peer,
		parentPeer,
		guildId,
		teamId,
		memberRoleIds,
		dmScope
	}) : "";
	if (routeCache && routeCacheKey) {
		const cachedRoute = routeCache.get(routeCacheKey);
		if (cachedRoute) return { ...cachedRoute };
	}
	const bindings = getEvaluatedBindingsForChannelAccount(input.cfg, channel, accountId);
	const bindingsIndex = getEvaluatedBindingIndexForChannelAccount(input.cfg, channel, accountId);
	const choose = (agentId, matchedBy) => {
		const resolvedAgentId = pickFirstExistingAgentId(input.cfg, agentId);
		const route = {
			agentId: resolvedAgentId,
			channel,
			accountId,
			sessionKey: buildAgentSessionKey({
				agentId: resolvedAgentId,
				channel,
				accountId,
				peer,
				dmScope,
				identityLinks
			}).toLowerCase(),
			mainSessionKey: buildAgentMainSessionKey({
				agentId: resolvedAgentId,
				mainKey: DEFAULT_MAIN_KEY
			}).toLowerCase(),
			matchedBy
		};
		if (routeCache && routeCacheKey) {
			routeCache.set(routeCacheKey, route);
			if (routeCache.size > MAX_RESOLVED_ROUTE_CACHE_KEYS) {
				routeCache.clear();
				routeCache.set(routeCacheKey, route);
			}
		}
		return route;
	};
	const formatPeer = (value) => value?.kind && value?.id ? `${value.kind}:${value.id}` : "none";
	const formatNormalizedPeer = (value) => {
		if (value.state === "none") return "none";
		if (value.state === "invalid") return "invalid";
		return `${value.kind}:${value.id}`;
	};
	if (shouldLogDebug) {
		logDebug(`[routing] resolveAgentRoute: channel=${channel} accountId=${accountId} peer=${formatPeer(peer)} guildId=${guildId || "none"} teamId=${teamId || "none"} bindings=${bindings.length}`);
		for (const entry of bindings) logDebug(`[routing] binding: agentId=${entry.binding.agentId} accountPattern=${entry.match.accountPattern || "default"} peer=${formatNormalizedPeer(entry.match.peer)} guildId=${entry.match.guildId ?? "none"} teamId=${entry.match.teamId ?? "none"} roles=${entry.match.roles?.length ?? 0}`);
	}
	const baseScope = {
		guildId,
		teamId,
		memberRoleIds: memberRoleIdSet
	};
	const tiers = [
		{
			matchedBy: "binding.peer",
			enabled: Boolean(peer),
			scopePeer: peer,
			candidates: collectPeerIndexedBindings(bindingsIndex, peer),
			predicate: (candidate) => candidate.match.peer.state === "valid"
		},
		{
			matchedBy: "binding.peer.parent",
			enabled: Boolean(parentPeer && parentPeer.id),
			scopePeer: parentPeer && parentPeer.id ? parentPeer : null,
			candidates: collectPeerIndexedBindings(bindingsIndex, parentPeer),
			predicate: (candidate) => candidate.match.peer.state === "valid"
		},
		{
			matchedBy: "binding.guild+roles",
			enabled: Boolean(guildId && memberRoleIds.length > 0),
			scopePeer: peer,
			candidates: guildId ? bindingsIndex.byGuildWithRoles.get(guildId) ?? [] : [],
			predicate: (candidate) => hasGuildConstraint(candidate.match) && hasRolesConstraint(candidate.match)
		},
		{
			matchedBy: "binding.guild",
			enabled: Boolean(guildId),
			scopePeer: peer,
			candidates: guildId ? bindingsIndex.byGuild.get(guildId) ?? [] : [],
			predicate: (candidate) => hasGuildConstraint(candidate.match) && !hasRolesConstraint(candidate.match)
		},
		{
			matchedBy: "binding.team",
			enabled: Boolean(teamId),
			scopePeer: peer,
			candidates: teamId ? bindingsIndex.byTeam.get(teamId) ?? [] : [],
			predicate: (candidate) => hasTeamConstraint(candidate.match)
		},
		{
			matchedBy: "binding.account",
			enabled: true,
			scopePeer: peer,
			candidates: bindingsIndex.byAccount,
			predicate: (candidate) => candidate.match.accountPattern !== "*"
		},
		{
			matchedBy: "binding.channel",
			enabled: true,
			scopePeer: peer,
			candidates: bindingsIndex.byChannel,
			predicate: (candidate) => candidate.match.accountPattern === "*"
		}
	];
	for (const tier of tiers) {
		if (!tier.enabled) continue;
		const matched = tier.candidates.find((candidate) => tier.predicate(candidate) && matchesBindingScope(candidate.match, {
			...baseScope,
			peer: tier.scopePeer
		}));
		if (matched) {
			if (shouldLogDebug) logDebug(`[routing] match: matchedBy=${tier.matchedBy} agentId=${matched.binding.agentId}`);
			return choose(matched.binding.agentId, tier.matchedBy);
		}
	}
	return choose(resolveDefaultAgentId(input.cfg), "default");
}

//#endregion
export { resolveAgentRoute as n, resolve_route_exports as r, buildAgentSessionKey as t };