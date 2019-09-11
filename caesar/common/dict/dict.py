class DictDiffer(object):
    """
    diff dict by set
    """

    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    # return added
    def added(self):
        return self.set_current - self.intersect

    # return removed
    def removed(self):
        return self.set_past - self.intersect

    # return set of changed
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

    # return set of unchanged
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
