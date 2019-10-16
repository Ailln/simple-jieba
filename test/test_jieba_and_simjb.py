import jieba
import simjb
import torbjorn as tbn


def get_data(name):
    train_data_path = f"./icwb2-data/training/{name}_training.utf8"
    with open(train_data_path, "r") as f_data:
        datas = f_data.readlines()
    return datas


@tbn.run_time
def calc(datas, data_name, tool_name, tool):
    all_num = 0
    true_num = 0
    false_num = 0

    for data in datas:
        sentence_list = data.strip().split("  ")
        predict_list = list(tool.cut("".join(sentence_list)))

        sentence_pos_list = []
        sentence_len = 0
        for word in sentence_list:
            word_len = len(word)
            sentence_pos_list.append([sentence_len, sentence_len + word_len])
            sentence_len += word_len

        predict_pos_list = []
        predict_len = 0
        for word in predict_list:
            word_len = len(word)
            predict_pos_list.append([predict_len, predict_len + word_len])
            predict_len += word_len

        true_word_num = 0
        false_word_num = 0
        for pos in sentence_pos_list:
            if pos in predict_pos_list:
                true_word_num += 1
            else:
                false_word_num += 1

        all_num += len(sentence_pos_list)
        true_num += true_word_num
        false_num += false_word_num

    print(f"\n## {data_name} | {tool_name}")
    print(f">> all: {all_num}, true: {true_num}, false: {false_num}, acc: {true_num / all_num}")


def run():
    data_name_list = ["pku", "msr"]
    for data_name in data_name_list:
        datas = get_data(data_name)
        tools = {"jieba": jieba, "simjb": simjb}
        for tool_name, tool in tools.items():
            calc(datas, data_name, tool_name, tool)


if __name__ == '__main__':
    run()
